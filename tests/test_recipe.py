import pandas as pd

from wizcraft.recipe import Recipe, apply_recipe, apply_recipe_to_dataframe


def test_recipe_applies_multiple_steps_to_dataframe():
    df = pd.DataFrame(
        {
            "age": [10.0, None, 30.0],
            "city": ["Kolkata", "Delhi", "Kolkata"],
            "unused": [1, 2, 3],
        }
    )
    recipe = Recipe(
        steps=[
            {"action": "fill_null", "params": {"column": "age", "method": "mean"}},
            {"action": "one_hot_encode", "params": {"column": "city"}},
            {"action": "remove_column", "params": {"column": "unused"}},
            {
                "action": "scale",
                "params": {"columns": ["age"], "method": "normalize"},
            },
        ]
    )

    result = apply_recipe_to_dataframe(df, recipe)

    assert result.columns.tolist() == ["age", "city_Kolkata"]
    assert result["age"].tolist() == [0.0, 0.5, 1.0]
    assert result["city_Kolkata"].tolist() == [True, False, True]


def test_recipe_can_be_saved_and_applied_to_csv(tmp_path):
    input_csv = tmp_path / "input.csv"
    recipe_json = tmp_path / "recipe.json"
    output_csv = tmp_path / "output.csv"
    pd.DataFrame({"score": [5.0, None, 15.0]}).to_csv(input_csv, index=False)
    Recipe(
        input_file=str(input_csv),
        steps=[
            {
                "action": "fill_null",
                "params": {"column": "score", "method": "median"},
            }
        ],
    ).save(recipe_json)

    result = apply_recipe(input_csv, recipe_json, output_csv)

    assert result["score"].tolist() == [5.0, 10.0, 15.0]
    assert pd.read_csv(output_csv)["score"].tolist() == [5.0, 10.0, 15.0]
