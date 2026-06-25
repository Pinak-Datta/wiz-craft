import json

import pandas as pd

from wizcraft.doctor import inspect_dataset, write_recipe


def test_doctor_finds_issues_and_builds_recipe(tmp_path):
    csv_file = tmp_path / "train.csv"
    pd.DataFrame(
        {
            "row_id": [1, 2, 3, 4, 5],
            "age": [10.0, None, 30.0, 40.0, 1000.0],
            "city": ["Kolkata", "Delhi", "Kolkata", "Mumbai", "Delhi"],
            "mostly_missing": [None, None, None, None, "x"],
            "target": [1, 1, 1, 1, 0],
        }
    ).to_csv(csv_file, index=False)

    report = inspect_dataset(csv_file, target="target")

    messages = [issue.message for issue in report.issues]
    steps = report.recipe.steps
    assert report.rows == 5
    assert report.columns == 5
    assert report.score < 100
    assert any("missing value" in message for message in messages)
    assert any("identifier" in message for message in messages)
    assert any("imbalanced" in message for message in messages)
    assert {"action": "fill_null", "params": {"column": "age", "method": "median"}} in steps
    assert {
        "action": "one_hot_encode",
        "params": {"column": "city", "drop_first": True},
    } in steps
    assert {
        "action": "remove_column",
        "params": {"column": "row_id"},
    } in steps


def test_doctor_writes_recipe_json(tmp_path):
    csv_file = tmp_path / "train.csv"
    recipe_file = tmp_path / "recipe.json"
    pd.DataFrame({"score": [1.0, None, 3.0]}).to_csv(csv_file, index=False)
    report = inspect_dataset(csv_file)

    write_recipe(report, recipe_file)

    data = json.loads(recipe_file.read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert data["steps"] == [
        {"action": "fill_null", "params": {"column": "score", "method": "median"}}
    ]
