# categorical.py

import pandas as pd


class EncodeCategoricalValues:
    def __init__(self, dataset):
        self.dataset = dataset.copy()

    def show_categorical_columns(self):
        categorical_columns = self.dataset.select_dtypes(include='object').columns.tolist()
        print("\nCategorical columns present in the dataset:")
        for col in categorical_columns:
            print("-", col)

    def perform_one_hot_encoding(self):
        column_name = input("\nEnter the column name to perform one-hot encoding: ")

        if column_name not in self.dataset.columns:
            print(f"Error: Column '{column_name}' not found in the dataset.")
            return

        if pd.api.types.is_object_dtype(self.dataset[column_name]):
            encoded_column = pd.get_dummies(self.dataset[column_name], prefix=column_name, drop_first=True)
            self.dataset.drop(column_name, axis=1, inplace=True)
            self.dataset = pd.concat([self.dataset, encoded_column], axis=1)
            print(f"One-hot encoding applied for column '{column_name}'.")
            # encoded_column = pd.get_dummies(self.dataset[column_name], prefix=column_name, drop_first=True)
            # print(encoded_column)
            # self.dataset.drop(column_name, axis=1, inplace=True)
            # self.dataset = pd.concat([self.dataset, encoded_column], axis=1)
            return self.dataset
        else:
            print(f"Error: Column '{column_name}' is not a categorical column. Cannot perform one-hot encoding.")

    def show_dataset(self):
        n_rows = int(input("Enter the number of rows to show: "))
        print(self.dataset.head(n_rows))

    def display_menu(self):
        print("\n----Categorical data encoding tasks:----")
        print("1: Show categorical columns")
        print("2: Perform one-hot encoding for a column")
        print("3: Show the dataset")
        print("To go back to the previous menu, press -1")


if __name__ == "__main__":
    # For testing the EncodeCategoricalValues class
    df = pd.DataFrame({'Category': ['A', 'B', 'A', 'C'],
                       'Value': [10, 20, 30, 40]})

    categorical_encoder = EncodeCategoricalValues(df)
    categorical_encoder.show_categorical_columns()
    df=categorical_encoder.perform_one_hot_encoding()
    categorical_encoder.show_dataset()
