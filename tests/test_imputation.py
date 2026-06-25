import pandas as pd

from wizcraft.imputation import DataImputation


def test_fill_null_with_mean_updates_numeric_column():
    df = pd.DataFrame({"age": [10.0, None, 40.0]})

    result = DataImputation(df).fill_null_with_mean("age")

    assert result["age"].tolist() == [10.0, 25.0, 40.0]


def test_fill_null_with_mode_updates_categorical_column():
    df = pd.DataFrame({"city": ["Kolkata", None, "Kolkata", "Delhi"]})

    result = DataImputation(df).fill_null_with_mode("city")

    assert result["city"].tolist() == ["Kolkata", "Kolkata", "Kolkata", "Delhi"]


def test_remove_column_drops_existing_column():
    df = pd.DataFrame({"keep": [1], "drop": [2]})

    result = DataImputation(df).remove_column("drop")

    assert result.columns.tolist() == ["keep"]
