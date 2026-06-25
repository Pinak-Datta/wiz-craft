import pandas as pd

from wizcraft.categorical import EncodeCategoricalValues
from wizcraft.feature_selection import FeatureScaling


def test_one_hot_encoding_returns_encoded_dataset():
    df = pd.DataFrame({"color": ["red", "blue", "red"], "score": [1, 2, 3]})

    result = EncodeCategoricalValues(df).perform_one_hot_encoding("color")

    assert "color" not in result.columns
    assert "color_red" in result.columns
    assert result["color_red"].tolist() == [True, False, True]


def test_normalization_scales_selected_columns():
    df = pd.DataFrame({"score": [10.0, 20.0, 30.0], "label": ["a", "b", "c"]})

    result = FeatureScaling(df).perform_normalization(["score"])

    assert result["score"].tolist() == [0.0, 0.5, 1.0]
