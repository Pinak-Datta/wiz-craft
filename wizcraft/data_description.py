# data_description.py

import pandas as pd


class DataDescription:
    def __init__(self, dataset):
        self.dataset = dataset

    def show_properties(self):
        print("\nProperties of each numeric column:")
        numeric_columns = self.dataset.select_dtypes(include='number')
        for col in numeric_columns.columns:
            print(f"Column: {col}")
            print("Data type:", numeric_columns[col].dtype)
            print("Null value count:", numeric_columns[col].isnull().sum())
            print("Mean:", numeric_columns[col].mean())
            print("Standard Deviation:", numeric_columns[col].std())
            print("Percentiles:")
            print(numeric_columns[col].quantile([0.25, 0.50, 0.75]))
            print("\nTotal number of values:", len(numeric_columns[col]))
            print("Maximum:", numeric_columns[col].max())
            print("Minimum:", numeric_columns[col].min())
            print()

    def show_column_properties(self, column_name):
        if column_name not in self.dataset.columns:
            print(f"Error: Column '{column_name}' not found in the dataset.")
            return

        column = self.dataset[column_name]
        print(f"\nProperties of column '{column_name}':")
        print("Data type:", column.dtype)
        print("Null value count:", column.isnull().sum())

        if pd.api.types.is_numeric_dtype(column):
            print("Mean:", column.mean())
            print("Standard Deviation:", column.std())
            print("Percentiles:")
            print(column.quantile([0.25, 0.50, 0.75]))
            print("Total number of values:", len(column))
            print("Maximum:", column.max())
            print("Minimum:", column.min())
        else:
            print("Total number of values:", len(column))
            print("Number of distinct values:", column.nunique())

    def show_dataset_rows(self, n):
        try:
            n = int(n)
            print(f"\nShowing first {n} rows of the dataset:")
            print(self.dataset.head(n))
        except ValueError:
            print("Error: Invalid input. Please enter a valid number of rows.")

    def display_menu(self):
        print("\n ----Data Description----")
        print("1: Describe a specific column")
        print("2: Show properties of each column")
        print("3: Show the dataset")
        print()
        print("(To return to previous menu, press -1)")


if __name__ == "__main__":
    # For testing the DataDescription class
    df = pd.DataFrame({'NumericCol': [1, 2, 3, 4, 5],
                       'StringCol': ['A', 'B', 'C', 'D', 'E']})

    data_description = DataDescription(df)
    data_description.show_properties()
    data_description.show_column_properties('NumericCol')
    data_description.show_column_properties('StringCol')
    data_description.show_dataset_rows(3)
