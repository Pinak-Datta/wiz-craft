import json
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


RECIPE_VERSION = 1


class Recipe:
    def __init__(self, input_file=None, target_variable=None, steps=None):
        self.input_file = input_file
        self.target_variable = target_variable
        self.steps = steps or []

    def add_step(self, action, confidence=None, **params):
        step = {"action": action, "params": params}
        if confidence is not None:
            step["confidence"] = confidence
        self.steps.append(step)

    def to_dict(self):
        return {
            "version": RECIPE_VERSION,
            "input_file": self.input_file,
            "target_variable": self.target_variable,
            "steps": self.steps,
        }

    def save(self, path):
        recipe_path = Path(path)
        recipe_path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return recipe_path

    @classmethod
    def load(cls, path):
        recipe_path = Path(path)
        data = json.loads(recipe_path.read_text(encoding="utf-8"))
        version = data.get("version")
        if version != RECIPE_VERSION:
            raise ValueError(
                f"Unsupported recipe version {version}. Expected {RECIPE_VERSION}."
            )
        return cls(
            input_file=data.get("input_file"),
            target_variable=data.get("target_variable"),
            steps=data.get("steps", []),
        )


def apply_recipe_to_dataframe(dataset, recipe):
    transformed = dataset.copy()

    for step in recipe.steps:
        action = step.get("action")
        params = step.get("params", {})

        if action == "remove_column":
            column = params["column"]
            _require_columns(transformed, [column])
            transformed = transformed.drop(columns=[column])
        elif action == "fill_null":
            transformed = _apply_fill_null(transformed, params)
        elif action == "one_hot_encode":
            column = params["column"]
            drop_first = params.get("drop_first", True)
            _require_columns(transformed, [column])
            encoded = pd.get_dummies(
                transformed[column], prefix=column, drop_first=drop_first
            )
            transformed = pd.concat(
                [transformed.drop(columns=[column]), encoded], axis=1
            )
        elif action == "scale":
            transformed = _apply_scale(transformed, params)
        else:
            raise ValueError(f"Unknown recipe action: {action}")

    return transformed


def apply_recipe(input_csv, recipe_path, output_csv):
    recipe = Recipe.load(recipe_path)
    dataset = pd.read_csv(input_csv)
    transformed = apply_recipe_to_dataframe(dataset, recipe)
    transformed.to_csv(output_csv, index=False)
    return transformed


def _apply_fill_null(dataset, params):
    column = params["column"]
    method = params["method"]
    _require_columns(dataset, [column])

    if method == "mean":
        _require_numeric(dataset, [column])
        dataset[column] = dataset[column].fillna(dataset[column].mean())
    elif method == "median":
        _require_numeric(dataset, [column])
        dataset[column] = dataset[column].fillna(dataset[column].median())
    elif method == "mode":
        mode = dataset[column].mode(dropna=True)
        if mode.empty:
            raise ValueError(f"Column '{column}' has no mode value.")
        dataset[column] = dataset[column].fillna(mode.iloc[0])
    elif method == "knn":
        from sklearn.impute import KNNImputer

        _require_numeric(dataset, [column])
        n_neighbors = params.get("n_neighbors", 5)
        imputer = KNNImputer(n_neighbors=n_neighbors)
        dataset[column] = imputer.fit_transform(dataset[[column]])
    else:
        raise ValueError(f"Unknown fill_null method: {method}")

    return dataset


def _apply_scale(dataset, params):
    columns = params["columns"]
    method = params["method"]
    _require_columns(dataset, columns)
    _require_numeric(dataset, columns)

    if method == "normalize":
        scaler = MinMaxScaler()
    elif method == "standardize":
        scaler = StandardScaler()
    else:
        raise ValueError(f"Unknown scale method: {method}")

    dataset[columns] = scaler.fit_transform(dataset[columns])
    return dataset


def _require_columns(dataset, columns):
    missing = [column for column in columns if column not in dataset.columns]
    if missing:
        raise ValueError(f"Missing column(s): {', '.join(missing)}")


def _require_numeric(dataset, columns):
    non_numeric = [
        column for column in columns if not pd.api.types.is_numeric_dtype(dataset[column])
    ]
    if non_numeric:
        raise ValueError(f"Column(s) must be numeric: {', '.join(non_numeric)}")
