# imputation.py

import pandas as pd


class DataImputation:
    def __init__(self, dataset):
        self.dataset = dataset

    def show_null_values_count(self):
        print("\nNumber of null values in each column:")
        null_counts = self.dataset.isnull().sum()
        print(null_counts)

    def remove_column(self, column_name):
        if column_name not in self.dataset.columns:
            print(f"Error: Column '{column_name}' not found in the dataset.")
            return

        self.dataset.drop(column_name, axis=1, inplace=True)
        print(f"Column '{column_name}' removed from the dataset.")

    def fill_null_with_mean(self, column_name):
        if column_name not in self.dataset.columns:
            print(f"Error: Column '{column_name}' not found in the dataset.")
            return

        if pd.api.types.is_numeric_dtype(self.dataset[column_name]):
            self.dataset[column_name].fillna(self.dataset[column_name].mean(), inplace=True)
            print(f"\nNull values in column '{column_name}' filled with the mean.")
        else:
            print(f"\nError: Column '{column_name}' is not numeric. Cannot fill with mean.")

    def fill_null_with_median(self, column_name):
        if column_name not in self.dataset.columns:
            print(f"\nError: Column '{column_name}' not found in the dataset.")
            return

        if pd.api.types.is_numeric_dtype(self.dataset[column_name]):
            self.dataset[column_name].fillna(self.dataset[column_name].median(), inplace=True)
            print(f"\nNull values in column '{column_name}' filled with the median.")
        else:
            print(f"\nError: Column '{column_name}' is not numeric. Cannot fill with median.")

    def fill_null_with_mode(self, column_name):
        if column_name not in self.dataset.columns:
            print(f"\nError: Column '{column_name}' not found in the dataset.")
            return

        self.dataset[column_name].fillna(self.dataset[column_name].mode().iloc[0], inplace=True)
        print(f"\nNull values in column '{column_name}' filled with the mode.")

    def display_menu(self):
        print("\n----Imputation tasks----:")
        print("1: Show number of null values")
        print("2: Remove columns")
        print("3: Fill Null values with mean")
        print("4: Fill Null values with median")
        print("5: Fill Null values with mode")
        print()
        print("(To go back to the previous menu, press -1)")


# if __name__ == "__main__":
#     # For testing the DataImputation class
#     df = pd.DataFrame({'NumericCol': [1, 2, None, 4, 5],
#                        'StringCol': ['A', 'B', 'C', None, 'E']})
#
#     data_imputation = DataImputation(df)
#     data_imputation.show_null_values_count()
#     data_imputation.remove_column('StringCol')
#     data_imputation.fill_null_with_mean('NumericCol')
#     data_imputation.fill_null_with_median('NumericCol')
#     data_imputation.fill_null_with_mode('StringCol')
