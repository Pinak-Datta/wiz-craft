import json

import pandas as pd

from wizcraft.doctor import (
    inspect_dataset,
    report_to_dict,
    write_html_report,
    write_json_report,
    write_recipe,
)


def test_doctor_finds_issues_and_builds_recipe(tmp_path):
    csv_file = tmp_path / "train.csv"
    pd.DataFrame(
        {
            "row_id": [1, 2, 3, 4, 5],
            "age": [10.0, None, 30.0, 40.0, 1000.0],
            "city": ["Kolkata", "Delhi", "Kolkata", "Mumbai", "Delhi"],
            "mostly_missing": [None, None, None, None, "x"],
            "signup_date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04", "2026-01-05"],
            "constant_flag": ["yes", "yes", "yes", "yes", "yes"],
            "target_score": [0.99, 0.98, 0.97, 0.96, 0.01],
            "target": [1, 1, 1, 1, 0],
        }
    ).to_csv(csv_file, index=False)

    report = inspect_dataset(csv_file, target="target")

    messages = [issue.message for issue in report.issues]
    steps = report.recipe.steps
    assert report.rows == 5
    assert report.columns == 8
    assert report.score < 100
    assert report.suggested_task == "Binary classification"
    assert any("missing value" in message for message in messages)
    assert any("identifier" in message for message in messages)
    assert any("imbalanced" in message for message in messages)
    assert any(issue.category == "Datetime" for issue in report.issues)
    assert any(issue.category == "Constant" for issue in report.issues)
    assert any(issue.category == "Leakage" for issue in report.issues)
    assert any(profile.inferred_type == "datetime" for profile in report.column_profiles)
    assert any(
        step["action"] == "fill_null"
        and step["params"] == {"column": "age", "method": "median"}
        and step["confidence"] == "high"
        for step in steps
    )
    assert any(
        step["action"] == "one_hot_encode"
        and step["params"] == {"column": "city", "drop_first": True}
        and step["confidence"] == "medium"
        for step in steps
    )
    assert any(
        step["action"] == "remove_column"
        and step["params"] == {"column": "row_id"}
        and step["confidence"] == "high"
        for step in steps
    )


def test_doctor_writes_recipe_json(tmp_path):
    csv_file = tmp_path / "train.csv"
    recipe_file = tmp_path / "recipe.json"
    pd.DataFrame({"score": [1.0, None, 3.0]}).to_csv(csv_file, index=False)
    report = inspect_dataset(csv_file)

    write_recipe(report, recipe_file)

    data = json.loads(recipe_file.read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert data["steps"] == [
        {
            "action": "fill_null",
            "params": {"column": "score", "method": "median"},
            "confidence": "high",
        }
    ]


def test_doctor_report_can_be_serialized_to_json(tmp_path):
    csv_file = tmp_path / "train.csv"
    report_file = tmp_path / "report.json"
    pd.DataFrame({"target": [1, 0], "category": ["a", "b"]}).to_csv(
        csv_file, index=False
    )
    report = inspect_dataset(csv_file, target="target")

    write_json_report(report, report_file)
    data = json.loads(report_file.read_text(encoding="utf-8"))

    assert data == report_to_dict(report)
    assert data["suggested_task"] == "Binary classification"
    assert data["column_profiles"][0]["column"] == "target"


def test_doctor_report_can_be_exported_to_html(tmp_path):
    csv_file = tmp_path / "train.csv"
    html_file = tmp_path / "report.html"
    pd.DataFrame({"target": [1, 0], "category": ["a", "b"]}).to_csv(
        csv_file, index=False
    )
    report = inspect_dataset(csv_file, target="target")

    write_html_report(report, html_file)

    html = html_file.read_text(encoding="utf-8")
    assert "Dataset Health Score" in html
    assert "Suggested Cleaning Recipe" in html
