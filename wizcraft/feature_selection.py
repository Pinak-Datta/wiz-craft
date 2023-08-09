# feature_selection.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


class FeatureScaling:
    def __init__(self, dataset):
        self.dataset = dataset.copy()

    def perform_normalization(self, column_names):
        try:
            scaler = MinMaxScaler()
            self.dataset[column_names] = scaler.fit_transform(self.dataset[column_names])
            print(f"\nNormalization (Min-Max scaling) applied to column(s): {', '.join(column_names)}.")
        except KeyError:
            print("Error: One or more specified columns not found in the dataset.")
        except ValueError:
            print("Error: The specified columns must be numeric.")

    def perform_standardization(self, column_names):
        try:
            scaler = StandardScaler()
            self.dataset[column_names] = scaler.fit_transform(self.dataset[column_names])
            print(f"\nStandardization (Standard Scaler) applied to column(s): {', '.join(column_names)}.")
        except KeyError:
            print("\nError: One or more specified columns not found in the dataset.")
        except ValueError:
            print("\nError: The specified columns must be numeric.")

    def show_dataset(self):
        n_rows = int(input("\nEnter the number of rows to show: "))
        print(self.dataset.head(n_rows))

    def display_menu(self):
        print("\n---Feature Scaling tasks---")
        print("1: Perform Normalization (Min-Max scaling)")
        print("2: Perform Standardization (Standard Scaler)")
        print("3: Show the dataset")
        print("\nTo go back to the previous menu, press -1")


if __name__ == "__main__":
    # For testing the FeatureScaling class
    df = pd.DataFrame({'Column1': [1, 2, 3, 4, 5],
                       'Column2': [10, 20, 30, 40, 50],
                       'Column3': [100, 200, 300, 400, 500]})

    feature_scaling = FeatureScaling(df)
    feature_scaling.perform_normalization(['Column1', 'Column2'])
    feature_scaling.perform_standardization(['Column3'])
    print(feature_scaling.dataset)
