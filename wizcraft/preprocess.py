# WizCraft.py
import os

import pandas as pd
import sys
from wizcraft.data_description import DataDescription
from wizcraft.categorical import EncodeCategoricalValues
from wizcraft.download import DownloadDataset
from wizcraft.feature_selection import FeatureScaling
from wizcraft.imputation import DataImputation
from wizcraft.io import Output, print_splash


class Preprocess:
    def __init__(self):
        self.original_dataset = None
        self.dataset = None
        self.target_variable = None
        self.output = Output()

    # @staticmethod
    # def clear_terminal():
    #     os.system('cls' if os.name == 'nt' else 'clear')

    def welcome_message(self):
        # self.clear_terminal()
        print_splash()

    # def display_columns(self):
    #     if self.dataset is not None:
    #         print("Columns present in the dataset:")
    #         for col in self.dataset.columns:
    #             print("-", col)
    #     else:
    #         print("Error: No dataset loaded. Please load the dataset first.")

    def get_csvs(self):
        # Function to get the list of CSV files present in the current directory
        csv_files = []
        for file in os.listdir("."):
            if file.endswith(".csv"):
                csv_files.append(file)
        return csv_files

    def load_dataset_from_command_line(self):
        # Function to load the dataset from the command line
        try:
            file_path = self.output.ask(
                "Enter the path of the CSV file",
                # default=self.get_csvs()[0],
                choices=self.get_csvs(),
                color="blue",
            )
            self.load_dataset(file_path)
        except Exception as e:
            print("Error:", e)

    def load_dataset(self, csv_file):
        try:
            # self.original_dataset = pd.read_csv(csv_file)
            self.dataset = pd.read_csv(csv_file)
            # self.dataset = self.original_dataset
            self.output.c_print("Dataset loaded [green]successfully[/green]\n")
        except FileNotFoundError:
            self.output.c_print(
                "[red]Error[/red]: File not found. Please check the [underline]file path[/underline] and try again."
            )
            # Actually exit the program because the dataset is not loaded
            # The whole program depends on the dataset
            # Exit the program with a non-zero exit code
            sys.exit(1)

    def choose_target_variable(self):
        # Function to choose the target (dependent) variable
        if self.dataset is not None:
            data = dict(
                cols=[],
                rows=[],
            )
            max_index = len(self.dataset.columns)
            for idx, col in enumerate(self.dataset.columns, 1):
                data["cols"].append(
                    {"name": f"{idx}. {col}", "justify": "center", "style": "red"}
                )

            self.output.display_table("Columns present in the dataset", data)

            target_idx = (
                int(
                    self.output.ask(
                        "\nTarget Variable Index",
                        choices=[str(i) for i in range(1, max_index + 1)],
                    )
                )
                - 1
            )

            if target_idx == -1:
                sys.exit("\nExiting the program....")
            elif target_idx in range(len(self.dataset.columns)):
                self.target_variable = self.dataset.columns[target_idx]
                self.output.c_print(
                    f"Target [underline]variable[/underline] [blue]{self.target_variable}[/blue] chose\n"
                )
            else:
                self.output.c_print(
                    "[red]Error[/red]: Invalid index. Please select a valid index."
                )
        else:
            self.output.c_print(
                "[red]Error[/red]: Dataset is not loaded. Please load the dataset first using 'load_dataset' function."
            )

    def display_menu(self):
        options = "\n".join(
            [
                "1. Data Description",
                "2. Handle Null Values",
                "3. Encode Categorical Values",
                "4. Feature Scale dataset",
                "5. Download the modified Dataset",
                "-1. Exit",
            ]
        )
        self.output.show_panel("Menu", content=options, color="green")

    def start(self):
        self.welcome_message()
        self.load_dataset_from_command_line()
        # self.display_columns()
        self.choose_target_variable()

        while True:
            self.display_menu()
            option = int(self.output.ask("Enter the option"))

            if option == -1:
                sys.exit("Exiting the program.")
            elif option == 1:
                self.perform_data_description()
            elif option == 2:
                self.perform_handle_null_values()
            elif option == 3:
                self.perform_categorical_encoding()
            elif option == 4:
                self.perform_feature_scaling()
            elif option == 5:
                self.perform_dataset_download()
            else:
                print("Invalid option. Please choose a valid option.")

    def perform_data_description(self):
        data_description = DataDescription(self.dataset)

        data_description.display_menu()
        option = self.output.ask("\nEnter the option")

        if option == "-1":
            return
        option = int(option)
        if option == 1:
            column_name = self.output.ask(
                "Enter the [underline]column name[/underline] to describe: "
            )
            data_description.show_column_properties(column_name)
        elif option == 2:
            data_description.show_properties()
        elif option == 3:
            n_rows = input("Enter the number of rows to show: ")
            data_description.show_dataset_rows(n_rows)
        else:
            print("Invalid option. Please choose a valid option.")

    def perform_handle_null_values(self):
        data_imputation = DataImputation(self.dataset)
        while True:
            data_imputation.display_menu()
            option = self.output.ask("Enter the option")

            if option == "-1":
                self.output.c_print("Going back to the [yellow]previous menu[/yellow]")
                break

            try:
                option = int(option)
                if option == 1:
                    data_imputation.show_null_values_count()
                elif option == 2:
                    column_name = input("\nEnter the column name to remove: ")
                    data_imputation.remove_column(column_name)
                elif option == 3:
                    column_name = input("\nEnter the column name to fill with mean: ")
                    data_imputation.fill_null_with_mean(column_name)
                elif option == 4:
                    column_name = input("\nEnter the column name to fill with median: ")
                    data_imputation.fill_null_with_median(column_name)
                elif option == 5:
                    column_name = input("\nEnter the column name to fill with mode: ")
                    data_imputation.fill_null_with_mode(column_name)
                else:
                    print("Invalid option. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a valid option.")

    def perform_categorical_encoding(self):
        categorical_encoder = EncodeCategoricalValues(self.dataset)
        while True:
            categorical_encoder.display_menu()
            option = self.output.ask("\nEnter the option", color="yellow")

            if option == "-1":
                self.output.c_print(
                    "\nGoing back to the previous menu...", code="warning"
                )
                break

            try:
                option = int(option)
                if option == 1:
                    categorical_encoder.show_categorical_columns()
                elif option == 2:
                    # column_name = input("Enter the column name to perform one-hot encoding: ")
                    categorical_encoder.perform_one_hot_encoding()
                elif option == 3:
                    categorical_encoder.show_dataset()
                else:
                    print("Invalid option. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a valid option.")

    def perform_feature_scaling(self):
        feature_scaler = FeatureScaling(self.dataset)
        while True:
            feature_scaler.display_menu()
            option = self.output.ask("\nEnter the option", color="yellow")

            if option == "-1":
                self.output.c_print(
                    "\nGoing back to the previous menu....", code="warning"
                )
                break

            try:
                option = int(option)
                if option == 1:
                    column_names = self.output.ask(
                        "\nEnter the column name(s) to perform [underline]normalization[/underline] (comma-separated): "
                    )
                    column_names = [col.strip() for col in column_names.split(",")]
                    feature_scaler.perform_normalization(column_names)
                elif option == 2:
                    column_names = self.output.ask(
                        "\nEnter the column name(s) to perform [underline]standardization[/underline] ("
                        "comma-separated):"
                    )
                    column_names = [col.strip() for col in column_names.split(",")]
                    feature_scaler.perform_standardization(column_names)
                elif option == 3:
                    feature_scaler.show_dataset()
                else:
                    self.output.c_print(
                        "Invalid option. Please choose a valid option.", code="danger"
                    )
            except ValueError:
                self.output.c_print(
                    "Invalid input. Please enter a valid option.", code="danger"
                )

    def perform_dataset_download(self):
        if self.dataset is not None:
            download_obj = DownloadDataset(self.dataset)
            filename = self.output.ask(
                "\nEnter the file name you want to give to the dataset: "
            )
            if filename == "-1":
                self.output.c_print(
                    "Going back to the previous menu...", code="warning"
                )
            else:
                download_obj.download_dataset(filename)
        else:
            self.output.c_print(
                "Error: Dataset is not loaded. Please load the dataset first using 'load_dataset' function.",
                code="danger",
            )


if __name__ == "__main__":
    project = Preprocess()
    project.start()
