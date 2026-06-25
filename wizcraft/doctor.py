import json
from io import StringIO
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from wizcraft.recipe import Recipe


@dataclass
class ColumnProfile:
    column: str
    inferred_type: str
    missing_rate: float
    unique_count: int


@dataclass
class DoctorIssue:
    severity: str
    column: str
    category: str
    message: str
    suggestion: str


@dataclass
class DoctorReport:
    csv_file: str
    rows: int
    columns: int
    score: int
    suggested_task: str = "Target not provided"
    column_profiles: list[ColumnProfile] = field(default_factory=list)
    issues: list[DoctorIssue] = field(default_factory=list)
    recipe: Optional[Recipe] = None


def inspect_dataset(csv_file, target=None, missing_drop_threshold=0.5):
    dataset = pd.read_csv(csv_file)
    issues = []
    recipe = Recipe(input_file=str(csv_file), target_variable=target)
    column_profiles = _profile_columns(dataset)
    profile_map = {profile.column: profile for profile in column_profiles}
    suggested_task = _detect_task(dataset, target)

    _inspect_duplicate_rows(dataset, issues)
    _inspect_missing_values(dataset, issues, recipe, missing_drop_threshold)
    _inspect_constant_columns(dataset, issues, recipe, target)
    _inspect_id_like_columns(dataset, issues, recipe, target)
    _inspect_date_columns(dataset, issues, target, profile_map)
    _inspect_categorical_columns(dataset, issues, recipe, target)
    _inspect_numeric_outliers(dataset, issues, target)
    _inspect_target(dataset, issues, target)
    _inspect_leakage(dataset, issues, target)

    score = _score_dataset(issues)
    return DoctorReport(
        csv_file=str(csv_file),
        rows=len(dataset),
        columns=len(dataset.columns),
        score=score,
        suggested_task=suggested_task,
        column_profiles=column_profiles,
        issues=issues,
        recipe=recipe,
    )


def write_recipe(report, output_path):
    report.recipe.save(output_path)
    return output_path


def write_json_report(report, output_path):
    output = Path(output_path)
    output.write_text(json.dumps(report_to_dict(report), indent=2), encoding="utf-8")
    return output


def write_html_report(report, output_path):
    output = Path(output_path)
    console = Console(record=True, width=100, file=StringIO(), force_terminal=True)
    render_report(report, console=console)
    html = console.export_html(
        inline_styles=True,
        code_format='<pre style="font-size:14px; line-height:1.25">{code}</pre>',
    )
    html = html.replace("<head>", "<head><title>WizCraft Dataset Doctor</title>", 1)
    output.write_text(html, encoding="utf-8")
    return output


def report_to_dict(report):
    return {
        "csv_file": report.csv_file,
        "rows": report.rows,
        "columns": report.columns,
        "score": report.score,
        "status": _score_status(report.score),
        "suggested_task": report.suggested_task,
        "column_profiles": [asdict(profile) for profile in report.column_profiles],
        "issues": [asdict(issue) for issue in report.issues],
        "recipe": report.recipe.to_dict() if report.recipe else None,
    }


def render_report(report, console=None):
    console = console or Console()
    score_color = _score_color(report.score)
    status = _score_status(report.score)
    summary = "\n".join(
        [
            f"[bold]{report.csv_file}[/bold]",
            f"{report.rows:,} rows x {report.columns:,} columns",
            f"Task: [bold]{report.suggested_task}[/bold]",
            f"Status: [{score_color}]{status}[/{score_color}]",
        ]
    )
    console.print(
        Panel(
            summary,
            title=f"Dataset Health Score: {report.score}/100",
            border_style=score_color,
        )
    )

    console.print(_build_summary_table(report))
    console.print(_build_type_table(report))

    if report.recipe and report.recipe.steps:
        recipe_table = Table(title="Suggested Cleaning Recipe (Safe Auto-Fixes)")
        recipe_table.add_column("#", justify="right", style="dim")
        recipe_table.add_column("Action", style="bold green")
        recipe_table.add_column("Detail")
        recipe_table.add_column("Confidence")
        for index, step in enumerate(report.recipe.steps, 1):
            recipe_table.add_row(
                str(index),
                _format_action(step["action"]),
                _format_params(step.get("params", {})),
                step.get("confidence", "medium").title(),
            )
        console.print(recipe_table)
        console.print(
            "[dim]Save this recipe with --write-recipe, then run it with wizcraft apply.[/dim]"
        )
    else:
        console.print("[yellow]No safe automatic recipe steps were suggested.[/yellow]")

    if not report.issues:
        console.print("[green]No major issues found.[/green]")
        return

    table = Table(title="Findings That Need Attention")
    table.add_column("Severity", style="bold")
    table.add_column("Column")
    table.add_column("Finding")
    table.add_column("Next step")

    for issue in report.issues:
        table.add_row(
            _format_severity(issue.severity),
            issue.column or "-",
            issue.message,
            issue.suggestion,
        )

    console.print(table)


def _profile_columns(dataset):
    return [
        ColumnProfile(
            column=column,
            inferred_type=_infer_column_type(dataset[column], column),
            missing_rate=float(dataset[column].isna().mean()),
            unique_count=int(dataset[column].nunique(dropna=True)),
        )
        for column in dataset.columns
    ]


def _infer_column_type(series, column_name):
    missing_rate = float(series.isna().mean())
    unique_count = int(series.nunique(dropna=True))
    lower_name = column_name.lower()

    if missing_rate >= 0.5:
        return "mostly_empty"
    if unique_count <= 1:
        return "constant"
    if lower_name == "id" or lower_name.endswith("_id"):
        return "id"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_numeric_dtype(series):
        if (
            pd.api.types.is_integer_dtype(series)
            and unique_count == len(series.dropna())
            and unique_count / max(len(series), 1) > 0.95
        ):
            return "id"
        return "numeric"
    if _looks_like_datetime(series):
        return "datetime"
    if _looks_text_like(series):
        return "text"
    return "categorical"


def _detect_task(dataset, target):
    if target is None:
        return "Target not provided"
    if target not in dataset.columns:
        return "Unknown: target missing"

    target_series = dataset[target].dropna()
    unique_count = int(target_series.nunique())
    if unique_count == 2:
        return "Binary classification"
    if pd.api.types.is_numeric_dtype(target_series) and unique_count > 20:
        return "Regression"
    if unique_count > 2:
        return "Multiclass classification"
    return "Unknown"


def _inspect_duplicate_rows(dataset, issues):
    duplicate_count = int(dataset.duplicated().sum())
    if duplicate_count:
        issues.append(
            DoctorIssue(
                severity="medium",
                column="",
                category="Duplicates",
                message=f"{duplicate_count:,} duplicate row(s) found.",
                suggestion="Review or remove duplicates.",
            )
        )


def _inspect_missing_values(dataset, issues, recipe, missing_drop_threshold):
    for column in dataset.columns:
        missing_count = int(dataset[column].isna().sum())
        if not missing_count:
            continue

        missing_rate = missing_count / len(dataset)
        if missing_rate >= missing_drop_threshold:
            issues.append(
                DoctorIssue(
                    severity="high",
                    column=column,
                    category="Missing",
                    message=f"{missing_rate:.1%} missing values.",
                    suggestion="Review before auto-fixing.",
                )
            )
            continue

        if pd.api.types.is_numeric_dtype(dataset[column]):
            method = "median"
            confidence = "high"
        else:
            method = "mode"
            confidence = "medium"

        recipe.add_step("fill_null", column=column, method=method, confidence=confidence)
        issues.append(
            DoctorIssue(
                severity="medium",
                column=column,
                category="Missing",
                message=f"{missing_count:,} missing value(s).",
                suggestion=f"Fill with {method}.",
            )
        )


def _inspect_constant_columns(dataset, issues, recipe, target):
    for column in dataset.columns:
        if column == target:
            continue

        value_counts = dataset[column].value_counts(normalize=True, dropna=True)
        if value_counts.empty:
            continue

        top_rate = float(value_counts.iloc[0])
        unique_count = int(dataset[column].nunique(dropna=True))
        if unique_count <= 1:
            recipe.add_step("remove_column", column=column, confidence="high")
            issues.append(
                DoctorIssue(
                    severity="medium",
                    column=column,
                    category="Constant",
                    message="Column has one distinct value.",
                    suggestion="Drop this column.",
                )
            )
        elif top_rate >= 0.95:
            issues.append(
                DoctorIssue(
                    severity="low",
                    column=column,
                    category="Near-constant",
                    message=f"Top value appears in {top_rate:.1%} of rows.",
                    suggestion="Review before keeping.",
                )
            )


def _inspect_id_like_columns(dataset, issues, recipe, target):
    for column in dataset.columns:
        if column == target:
            continue

        lower_name = column.lower()
        unique_rate = dataset[column].nunique(dropna=True) / max(len(dataset), 1)
        looks_named_like_id = lower_name == "id" or lower_name.endswith("_id")
        looks_unique_integer = (
            pd.api.types.is_integer_dtype(dataset[column]) and unique_rate > 0.95
        )

        if looks_named_like_id or looks_unique_integer:
            recipe.add_step("remove_column", column=column, confidence="high")
            issues.append(
                DoctorIssue(
                    severity="low",
                    column=column,
                    category="Identifier",
                    message="Column looks like an identifier.",
                    suggestion="Drop unless it carries signal.",
                )
            )


def _inspect_date_columns(dataset, issues, target, profile_map):
    for column, profile in profile_map.items():
        if column == target:
            continue
        if profile.inferred_type != "datetime":
            continue

        issues.append(
            DoctorIssue(
                severity="low",
                column=column,
                category="Datetime",
                message="Column looks like a date or datetime.",
                suggestion="Extract year/month/day features.",
            )
        )


def _inspect_categorical_columns(dataset, issues, recipe, target):
    for column in dataset.select_dtypes(include=["object", "category", "bool"]).columns:
        if column == target:
            continue
        if dataset[column].isna().mean() >= 0.5:
            continue
        if _looks_like_datetime(dataset[column]):
            continue

        cardinality = int(dataset[column].nunique(dropna=True))
        if cardinality <= 1:
            continue
        if cardinality <= 20:
            recipe.add_step(
                "one_hot_encode", column=column, drop_first=True, confidence="medium"
            )
            issues.append(
                DoctorIssue(
                    severity="low",
                    column=column,
                    category="Categorical",
                    message=f"Categorical column with {cardinality} distinct value(s).",
                    suggestion="One-hot encode.",
                )
            )
        else:
            issues.append(
                DoctorIssue(
                    severity="medium",
                    column=column,
                    category="Categorical",
                    message=f"High-cardinality categorical column with {cardinality} distinct value(s).",
                    suggestion="Review before encoding.",
                )
            )


def _inspect_numeric_outliers(dataset, issues, target):
    numeric_columns = dataset.select_dtypes(include="number").columns
    for column in numeric_columns:
        if column == target:
            continue

        series = dataset[column].dropna()
        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = int(((series < lower) | (series > upper)).sum())
        outlier_rate = outlier_count / len(series)

        if outlier_rate >= 0.05:
            issues.append(
                DoctorIssue(
                    severity="low",
                    column=column,
                    category="Outliers",
                    message=f"{outlier_count:,} potential outlier(s) by IQR.",
                    suggestion="Review or cap outliers.",
                )
            )


def _inspect_target(dataset, issues, target):
    if target is None:
        return

    if target not in dataset.columns:
        issues.append(
            DoctorIssue(
                severity="high",
                column=target,
                category="Target",
                message="Target column was not found.",
                suggestion="Check --target.",
            )
        )
        return

    target_series = dataset[target].dropna()
    if target_series.empty:
        issues.append(
            DoctorIssue(
                severity="high",
                column=target,
                category="Target",
                message="Target column has no non-null values.",
                suggestion="Choose another target.",
            )
        )
        return

    if target_series.nunique() <= 20:
        normalized = target_series.value_counts(normalize=True)
        majority_rate = float(normalized.iloc[0])
        if majority_rate >= 0.8:
            issues.append(
                DoctorIssue(
                    severity="medium",
                    column=target,
                    category="Target",
                    message=f"Target is imbalanced: top class is {majority_rate:.1%}.",
                    suggestion="Use stratified splits.",
                )
            )


def _inspect_leakage(dataset, issues, target):
    if target is None or target not in dataset.columns:
        return

    suspicious_names = {
        "label",
        "target",
        "prediction",
        "predicted",
        "probability",
        "score",
        "result",
        "outcome",
    }
    target_lower = target.lower()
    target_series = dataset[target]

    for column in dataset.columns:
        if column == target:
            continue

        lower_name = column.lower()
        if lower_name in suspicious_names or (
            target_lower in lower_name and lower_name != target_lower
        ):
            issues.append(
                DoctorIssue(
                    severity="medium",
                    column=column,
                    category="Leakage",
                    message="Column name looks target-related.",
                    suggestion="Check for data leakage.",
                )
            )

        if pd.api.types.is_numeric_dtype(dataset[column]) and pd.api.types.is_numeric_dtype(
            target_series
        ):
            aligned = dataset[[column, target]].dropna()
            if len(aligned) >= 4:
                correlation = abs(float(aligned[column].corr(aligned[target])))
                if correlation >= 0.95:
                    issues.append(
                        DoctorIssue(
                            severity="high",
                            column=column,
                            category="Leakage",
                            message=f"Highly correlated with target ({correlation:.2f}).",
                            suggestion="Verify this is not leakage.",
                        )
                    )


def _score_dataset(issues):
    penalty = 0
    for issue in issues:
        if issue.severity == "high":
            penalty += 18
        elif issue.severity == "medium":
            penalty += 9
        else:
            penalty += 3
    return max(0, 100 - penalty)


def _looks_like_datetime(series):
    sample = series.dropna().astype(str)
    if sample.empty:
        return False
    parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
    return float(parsed.notna().mean()) >= 0.8


def _looks_text_like(series):
    sample = series.dropna().astype(str)
    if sample.empty:
        return False
    average_length = float(sample.str.len().mean())
    unique_rate = sample.nunique() / max(len(sample), 1)
    return average_length >= 40 and unique_rate >= 0.5


def _score_color(score):
    if score >= 80:
        return "green"
    if score >= 60:
        return "yellow"
    return "red"


def _score_status(score):
    if score >= 80:
        return "Ready for preprocessing"
    if score >= 60:
        return "Usable with cleanup"
    return "Needs review before modeling"


def _build_summary_table(report):
    severity_counts = {"high": 0, "medium": 0, "low": 0}
    categories = set()
    for issue in report.issues:
        severity_counts[issue.severity] += 1
        categories.add(issue.category)

    table = Table(title="Audit Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value")
    table.add_row("High severity", str(severity_counts["high"]))
    table.add_row("Medium severity", str(severity_counts["medium"]))
    table.add_row("Low severity", str(severity_counts["low"]))
    table.add_row("Issue categories", ", ".join(sorted(categories)) or "-")
    table.add_row("Suggested recipe steps", str(len(report.recipe.steps)))
    return table


def _build_type_table(report):
    type_counts = {}
    type_examples = {}
    for profile in report.column_profiles:
        type_counts[profile.inferred_type] = type_counts.get(profile.inferred_type, 0) + 1
        type_examples.setdefault(profile.inferred_type, []).append(profile.column)

    table = Table(title="Detected Column Types")
    table.add_column("Type", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Examples")
    for inferred_type in sorted(type_counts):
        examples = ", ".join(type_examples[inferred_type][:4])
        if len(type_examples[inferred_type]) > 4:
            examples += ", ..."
        table.add_row(inferred_type, str(type_counts[inferred_type]), examples)
    return table


def _format_action(action):
    return action.replace("_", " ").title()


def _format_params(params):
    if "column" in params and "method" in params:
        return f"{params['column']} -> {params['method']}"
    if "column" in params and "drop_first" in params:
        return f"{params['column']} -> one-hot encode"
    if "column" in params:
        return str(params["column"])
    if "columns" in params and "method" in params:
        return f"{', '.join(params['columns'])} -> {params['method']}"
    return ", ".join(f"{key}={value}" for key, value in params.items())


def _format_severity(severity):
    colors = {"high": "red", "medium": "yellow", "low": "cyan"}
    return f"[{colors.get(severity, 'white')}]{severity.upper()}[/{colors.get(severity, 'white')}]"
