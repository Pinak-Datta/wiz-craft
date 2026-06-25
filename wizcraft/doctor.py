from dataclasses import dataclass, field

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from wizcraft.recipe import Recipe


@dataclass
class DoctorIssue:
    severity: str
    column: str
    message: str
    suggestion: str


@dataclass
class DoctorReport:
    csv_file: str
    rows: int
    columns: int
    score: int
    issues: list[DoctorIssue] = field(default_factory=list)
    recipe: Recipe | None = None


def inspect_dataset(csv_file, target=None, missing_drop_threshold=0.8):
    dataset = pd.read_csv(csv_file)
    issues = []
    recipe = Recipe(input_file=str(csv_file), target_variable=target)

    _inspect_duplicate_rows(dataset, issues)
    _inspect_missing_values(dataset, issues, recipe, missing_drop_threshold)
    _inspect_id_like_columns(dataset, issues, recipe, target)
    _inspect_categorical_columns(dataset, issues, recipe, target)
    _inspect_numeric_outliers(dataset, issues, target)
    _inspect_target(dataset, issues, target)

    score = _score_dataset(issues)
    return DoctorReport(
        csv_file=str(csv_file),
        rows=len(dataset),
        columns=len(dataset.columns),
        score=score,
        issues=issues,
        recipe=recipe,
    )


def write_recipe(report, output_path):
    report.recipe.save(output_path)
    return output_path


def render_report(report):
    console = Console()
    title = f"Dataset Health Score: {report.score}/100"
    summary = f"{report.rows:,} rows x {report.columns:,} columns\n{report.csv_file}"
    console.print(Panel(summary, title=title, border_style=_score_color(report.score)))

    if not report.issues:
        console.print("[green]No major issues found.[/green]")
        return

    table = Table(title="Doctor Findings")
    table.add_column("Severity", style="bold")
    table.add_column("Column")
    table.add_column("Issue")
    table.add_column("Suggestion")

    for issue in report.issues:
        table.add_row(
            _format_severity(issue.severity),
            issue.column or "-",
            issue.message,
            issue.suggestion,
        )

    console.print(table)

    if report.recipe and report.recipe.steps:
        recipe_table = Table(title="Suggested Recipe Steps")
        recipe_table.add_column("#", justify="right")
        recipe_table.add_column("Action")
        recipe_table.add_column("Parameters")
        for index, step in enumerate(report.recipe.steps, 1):
            recipe_table.add_row(
                str(index),
                step["action"],
                ", ".join(
                    f"{key}={value}" for key, value in step.get("params", {}).items()
                ),
            )
        console.print(recipe_table)


def _inspect_duplicate_rows(dataset, issues):
    duplicate_count = int(dataset.duplicated().sum())
    if duplicate_count:
        issues.append(
            DoctorIssue(
                severity="medium",
                column="",
                message=f"{duplicate_count:,} duplicate row(s) found.",
                suggestion="Review duplicates before model training.",
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
                    message=f"{missing_rate:.1%} missing values.",
                    suggestion="Consider dropping this column or collecting better data.",
                )
            )
            continue

        if pd.api.types.is_numeric_dtype(dataset[column]):
            method = "median"
        else:
            method = "mode"

        recipe.add_step("fill_null", column=column, method=method)
        issues.append(
            DoctorIssue(
                severity="medium",
                column=column,
                message=f"{missing_count:,} missing value(s).",
                suggestion=f"Fill missing values with {method}.",
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
            recipe.add_step("remove_column", column=column)
            issues.append(
                DoctorIssue(
                    severity="low",
                    column=column,
                    message="Column looks like an identifier.",
                    suggestion="Drop it before model training unless it carries signal.",
                )
            )


def _inspect_categorical_columns(dataset, issues, recipe, target):
    for column in dataset.select_dtypes(include=["object", "category", "bool"]).columns:
        if column == target:
            continue
        if dataset[column].isna().mean() >= 0.8:
            continue

        cardinality = int(dataset[column].nunique(dropna=True))
        if cardinality <= 1:
            issues.append(
                DoctorIssue(
                    severity="medium",
                    column=column,
                    message="Column has one or fewer distinct values.",
                    suggestion="Consider dropping this low-information column.",
                )
            )
        elif cardinality <= 20:
            recipe.add_step("one_hot_encode", column=column, drop_first=True)
            issues.append(
                DoctorIssue(
                    severity="low",
                    column=column,
                    message=f"Categorical column with {cardinality} distinct value(s).",
                    suggestion="One-hot encode this column.",
                )
            )
        else:
            issues.append(
                DoctorIssue(
                    severity="medium",
                    column=column,
                    message=f"High-cardinality categorical column with {cardinality} distinct value(s).",
                    suggestion="Review before encoding; one-hot encoding may create too many columns.",
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
                    message=f"{outlier_count:,} potential outlier(s) by IQR.",
                    suggestion="Review outliers; consider clipping or robust scaling.",
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
                message="Target column was not found.",
                suggestion="Check the --target value.",
            )
        )
        return

    target_series = dataset[target].dropna()
    if target_series.empty:
        issues.append(
            DoctorIssue(
                severity="high",
                column=target,
                message="Target column has no non-null values.",
                suggestion="Choose another target or fix the source data.",
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
                    message=f"Target is imbalanced: top class is {majority_rate:.1%}.",
                    suggestion="Use stratified splits and appropriate metrics.",
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


def _score_color(score):
    if score >= 80:
        return "green"
    if score >= 60:
        return "yellow"
    return "red"


def _format_severity(severity):
    colors = {"high": "red", "medium": "yellow", "low": "cyan"}
    return f"[{colors.get(severity, 'white')}]{severity.upper()}[/{colors.get(severity, 'white')}]"
