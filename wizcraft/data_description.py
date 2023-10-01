# data_description.py

import pandas as pd
from wizcraft.io import Output


class DataDescription:
    def __init__(self, dataset):
        self.dataset = dataset
        self.output = Output()

    def show_properties(self):
        self.output.c_print("\nProperties of each numeric column:", code="info")
        numeric_columns = self.dataset.select_dtypes(include="number")
        for col in numeric_columns.columns:
            self.show_column_properties(col)

    def show_column_properties(self, column_name):
        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"[red]Error[/red]: Column [underline]'{column_name}'[/underline] not found in the dataset."
            )
            return

        column = self.dataset[column_name]
        self.output.c_print(f"\nProperties of column [blue]{column_name}[/blue]:")
        self.output.c_print(f"Data type: [blue]{column.dtype}[/blue]")
        self.output.c_print(f"Null value count: [blue]{column.isnull().sum()}[/blue]\n")

        if pd.api.types.is_numeric_dtype(column):
            data = "\n".join(
                [
                    # Rounding to 5 decimal places
                    # Just for consistency !CAN BE REMOVED!
                    f"Mean: {str(round(column.mean(), 5))}",
                    f"Standard Deviation: {str(round(column.std(), 5))}",
                    f"Percentiles:\n{str(column.quantile([0.25, 0.50, 0.75]))}",
                    f"Total number of values: {str(len(column))}",
                    f"Maximum: {str(column.max())}",
                    f"Minimum: {str(column.min())}",
                ]
            )

            self.output.show_panel(
                f"Info about numeric column {column_name}",
                content=data,
                color="blue",
            )
        else:
            self.output.c_print("Total number of values:", len(column))
            self.output.c_print("Number of distinct values:", column.nunique())

    def show_dataset_rows(self, n):
        try:
            n = int(n)
            self.output.c_print(
                f"\nShowing first {n} rows of the dataset:", code="info"
            )
            self.output.c_print(self.dataset.head(n))
        except ValueError:
            print("Error: Invalid input. Please enter a valid number of rows.")

    def display_menu(self):
        print()
        options = "\n".join(
            [
                "1. Describe a specific column",
                "2. Show properties of each column",
                "3. Show the dataset",
                "-1. Return to previous menu",
            ]
        )

        self.output.show_panel("Data Description", options, color="blue")


if __name__ == "__main__":
    # For testing the DataDescription class
    df = pd.DataFrame(
        {"NumericCol": [1, 2, 3, 4, 5], "StringCol": ["A", "B", "C", "D", "E"]}
    )

    data_description = DataDescription(df)
    data_description.show_properties()
    data_description.show_column_properties("NumericCol")
    data_description.show_column_properties("StringCol")
    data_description.show_dataset_rows(3)
