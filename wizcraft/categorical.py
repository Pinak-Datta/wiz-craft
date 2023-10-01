# categorical.py
import random

import pandas as pd
from wizcraft.io import Output


class EncodeCategoricalValues:
    def __init__(self, dataset):
        self.dataset = dataset.copy()
        self.output = Output()

    def show_categorical_columns(self):
        # categorical_columns = self.dataset.select_dtypes(include='object').columns.tolist()
        data = dict(
            cols=[],
            rows=[],
        )
        for idx, col in enumerate(self.dataset.columns, 1):
            data["cols"].append(
                {"name": f"{idx}. {col}", "justify": "center", "style": "red"}
            )

        self.output.display_table("Columns present in the dataset", data)

    def perform_one_hot_encoding(self):
        column_name = self.output.ask(
            "\nEnter the column name to perform one-hot encoding", color="yellow"
        )

        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"Error: Column [underline]'{column_name}'[/underline] not found in the dataset.",
                code="danger",
            )
            return

        if pd.api.types.is_object_dtype(self.dataset[column_name]):
            encoded_column = pd.get_dummies(
                self.dataset[column_name], prefix=column_name, drop_first=True
            )
            self.dataset.drop(column_name, axis=1, inplace=True)
            self.dataset = pd.concat([self.dataset, encoded_column], axis=1)
            self.output.c_print(
                f"One-hot encoding applied for column '{column_name}'.", code="success"
            )
        else:
            self.output.c_print(
                f"Error: Column [underline]'{column_name}'[/underline] is not a categorical column. Cannot perform one-hot encoding.",
                code="danger",
            )

    def show_dataset(self):
        n_rows = int(input("Enter the number of rows to show: "))
        print()
        print(self.dataset.head(n_rows))
        print()

    def display_menu(self):
        options = "\n".join(
            [
                "1. Show categorical columns",
                "2. Perform one-hot encoding for a column",
                "3. Show the dataset",
                "-1. Return to previous menu",
            ]
        )
        self.output.show_panel(
            "Categorical data encoding tasks", content=options, color="blue"
        )


if __name__ == "__main__":
    # For testing the EncodeCategoricalValues class
    df = pd.DataFrame({"Category": ["A", "B", "A", "C"], "Value": [10, 20, 30, 40]})

    categorical_encoder = EncodeCategoricalValues(df)
    categorical_encoder.show_categorical_columns()
    categorical_encoder.perform_one_hot_encoding()
    categorical_encoder.show_dataset()
