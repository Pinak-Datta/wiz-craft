# feature_selection.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from wizcraft.io import Output


class FeatureScaling:
    def __init__(self, dataset):
        self.dataset = dataset.copy()
        self.output = Output()

    def perform_normalization(self, column_names):
        try:
            scaler = MinMaxScaler()
            self.dataset[column_names] = scaler.fit_transform(
                self.dataset[column_names]
            )
            self.output.c_print(
                f"\nNormalization (Min-Max scaling) applied to column(s): {', '.join(column_names)}.",
                code="success",
            )
        except KeyError:
            self.output.c_print(
                "Error: One or more specified columns not found in the dataset.",
                code="danger",
            )
        except ValueError:
            self.output.c_print(
                "Error: The specified columns must be numeric.", code="danger"
            )

    def perform_standardization(self, column_names):
        try:
            scaler = StandardScaler()
            self.dataset[column_names] = scaler.fit_transform(
                self.dataset[column_names]
            )
            self.output.c_print(
                f"\nStandardization (Standard Scaler) applied to column(s): {', '.join(column_names)}.",
                code="success",
            )
        except KeyError:
            self.output.c_print(
                "\nError: One or more specified columns not found in the dataset.",
                code="danger",
            )
        except ValueError:
            self.output.c_print(
                "\nError: The specified columns must be numeric.", code="danger"
            )

    def show_dataset(self):
        n_rows = int(self.output.ask("\nEnter the number of rows to show"))
        print(self.dataset.head(n_rows))

    def display_menu(self):
        options = "\n".join(
            [
                "1: Perform Normalization (Min-Max scaling)",
                "2: Perform Standardization (Standard Scaler)",
                "3: Show the dataset",
                "\nTo go back to the previous menu, press -1",
            ]
        )

        self.output.show_panel("Feature Scaling tasks", content=options, color="blue")


if __name__ == "__main__":
    # For testing the FeatureScaling class
    df = pd.DataFrame(
        {
            "Column1": [1, 2, 3, 4, 5],
            "Column2": [10, 20, 30, 40, 50],
            "Column3": [100, 200, 300, 400, 500],
        }
    )

    feature_scaling = FeatureScaling(df)
    feature_scaling.perform_normalization(["Column1", "Column2"])
    feature_scaling.perform_standardization(["Column3"])
    print(feature_scaling.dataset)
