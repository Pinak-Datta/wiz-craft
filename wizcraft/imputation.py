import pandas as pd
from sklearn.impute import KNNImputer

from wizcraft.io import Output


class DataImputation:
    def __init__(self, dataset):
        self.dataset = dataset
        self.output = Output()

    def show_null_values_count(self):
        self.output.c_print(
            "\nNumber of [underline]null[/underline] values in each column:"
        )
        null_counts = self.dataset.isnull().sum()
        print(null_counts)

    def remove_column(self, column_name):
        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"Error: Column [underline]'{column_name}'[/underline] not found in the dataset.",
                code="danger",
            )
            return self.dataset

        self.dataset.drop(column_name, axis=1, inplace=True)
        self.output.c_print(
            f"Column [underline]'{column_name}'[/underline] removed from the dataset.",
            code="success",
        )
        return self.dataset

    def fill_null_with_mean(self, column_name):
        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"Error: Column [underline]'{column_name}'[/underline] not found in the dataset.",
                code="danger",
            )
            return self.dataset

        if pd.api.types.is_numeric_dtype(self.dataset[column_name]):
            self.dataset[column_name] = self.dataset[column_name].fillna(
                self.dataset[column_name].mean()
            )
            self.output.c_print(
                f"\nNull values in column '{column_name}' filled with the mean.",
                code="success",
            )
        else:
            self.output.c_print(
                f"\nError: Column [underline]'{column_name}'[/underline] is not numeric. Cannot fill with median.",
                code="danger",
            )
        return self.dataset

    def fill_null_with_median(self, column_name):
        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"Error: Column [underline]'{column_name}'[/underline] not found in the dataset.",
                code="danger",
            )
            return self.dataset

        if pd.api.types.is_numeric_dtype(self.dataset[column_name]):
            self.dataset[column_name] = self.dataset[column_name].fillna(
                self.dataset[column_name].median()
            )
            self.output.c_print(
                f"\nNull values in column '{column_name}' filled with the median.",
                code="success",
            )
        else:
            self.output.c_print(
                f"\nError: Column [underline]'{column_name}'[/underline] is not numeric. Cannot fill with median.",
                code="danger",
            )
        return self.dataset

    def fill_null_with_mode(self, column_name):
        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"Error: Column [underline]'{column_name}'[/underline] not found in the dataset.",
                code="danger",
            )
            return self.dataset

        mode = self.dataset[column_name].mode(dropna=True)
        if mode.empty:
            self.output.c_print(
                f"\nError: Column [underline]'{column_name}'[/underline] has no mode value.",
                code="danger",
            )
            return self.dataset

        self.dataset[column_name] = self.dataset[column_name].fillna(mode.iloc[0])
        self.output.c_print(
            f"\nNull values in column '{column_name}' filled with the mode.",
            code="success",
        )
        return self.dataset

    def display_menu(self):
        options = "\n".join(
            [
                "1. Show number of null values",
                "2. Remove columns",
                "3. Fill Null values with mean",
                "4. Fill Null values with median",
                "5. Fill Null values with mode",
                "6. Fill Null values with K-nearest neighbors",
                "-1. Return to previous menu",
            ]
        )

        self.output.show_panel("Imputation tasks", content=options, color="blue")

    def fill_null_with_nearest_neighbors(self, column_name, n_neighbors):
        if column_name not in self.dataset.columns:
            self.output.c_print(
                f"\nError: Column [underline]'{column_name}'[/underline] not found in the dataset.",
                code="danger",
            )
            return self.dataset

        if pd.api.types.is_numeric_dtype(self.dataset[column_name]):
            imputer = KNNImputer(n_neighbors=n_neighbors)
            imputed_values = imputer.fit_transform(self.dataset[[column_name]])
            self.dataset[column_name] = imputed_values
            self.output.c_print(
                f"\nNull values in column '{column_name}' filled with nearest neighbors.",
                code="success",
            )
        else:
            self.output.c_print(
                f"\nError: Column [underline]'{column_name}'[/underline] is not numeric. Cannot fill with nearest neighbors.",
                code="danger",
            )
        return self.dataset

if __name__ == "__main__":
    # For testing the DataImputation class
    df = pd.DataFrame(
        {"NumericCol": [1, 2, None, 4, 5], "StringCol": ["A", "B", "C", None, "E"]}
    )

    data_imputation = DataImputation(df)
    # data_imputation.show_null_values_count()
    # data_imputation.remove_column('StringCol')
    # data_imputation.fill_null_with_mean('NumericCol')
    # data_imputation.fill_null_with_median('NumericCol')
    data_imputation.fill_null_with_nearest_neighbors('NumericCol', n_neighbors=2)
    data_imputation.fill_null_with_mode('StringCol')
    print(df)
