# WizCraft.py
import pandas as pd
import sys
from wizcraft.data_description import DataDescription
from wizcraft.categorical import EncodeCategoricalValues
from wizcraft.download import DownloadDataset
from wizcraft.feature_selection import FeatureScaling
from wizcraft.imputation import DataImputation


class Preprocess:
    def __init__(self):
        self.original_dataset = None
        self.dataset = None
        self.target_variable = None

    # @staticmethod
    # def clear_terminal():
    #     os.system('cls' if os.name == 'nt' else 'clear')

    def welcome_message(self):
        # self.clear_terminal()
        print()
        print("   __          ___        _____            __ _         ")
        print("   \ \        / (_)      / ____|          / _| |        ")
        print("    \ \  /\  / / _ ____ | |     _ __ __ _| |_| |_       ")
        print("     \ \/  \/ / | |_  / | |    | '__/ _` |  _| __|      ")
        print("  _ _ \  /\  /  | |/ /  | |____| | | (_| | | | |_ _ _ _ ")
        print(" (_|_|_)/  \/   |_/___|  \_____|_|  \__,_|_|  \__(_|_|_)")
        print("      Simplifying Data Preparation for ML Models \n")

    # def display_columns(self):
    #     if self.dataset is not None:
    #         print("Columns present in the dataset:")
    #         for col in self.dataset.columns:
    #             print("-", col)
    #     else:
    #         print("Error: No dataset loaded. Please load the dataset first.")

    def load_dataset_from_command_line(self):
        # Function to load the dataset from the command line
        try:
            file_path = input("Enter the path of the CSV file: ")
            self.load_dataset(file_path)
        except Exception as e:
            print("Error:", e)

    def load_dataset(self, csv_file):
        try:
            # self.original_dataset = pd.read_csv(csv_file)
            self.dataset = pd.read_csv(csv_file)
            # self.dataset = self.original_dataset
            print("Dataset loaded successfully...")
        except FileNotFoundError:
            print("Error: File not found. Please check the file path and try again.")

    def choose_target_variable(self):
        # Function to choose the target (dependent) variable
        if self.dataset is not None:
            print("Columns present in the dataset:")
            for idx, col in enumerate(self.dataset.columns, 1):
                print(f"{idx}. {col}")

            target_idx = int(input("Enter the index of the target variable (starting from 1): ")) - 1

            if target_idx == -1:
                sys.exit("\nExiting the program....")
            elif target_idx in range(len(self.dataset.columns)):
                self.target_variable = self.dataset.columns[target_idx]
                print(f"Selected target variable: {self.target_variable}")
            else:
                print("Error: Invalid index. Please select a valid index.")
        else:
            print("Error: Dataset is not loaded. Please load the dataset first using 'load_dataset' function.")

    def display_menu(self):
        print("\n----Menu----:")
        print("1. Data Description")
        print("2. Handle Null Values")
        print("3. Encode Categorical Values")
        print("4. Feature Scale dataset")
        print("5. Download the modified Dataset")
        print("-1. Exit")

    def start(self):
        self.welcome_message()
        self.load_dataset_from_command_line()
        # self.display_columns()
        self.choose_target_variable()

        while True:
            self.display_menu()
            option = int(input("Enter the option: "))

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
        option = input("\nEnter the option: ")

        if option == '-1':
            return
        option = int(option)
        if option == 1:
            column_name = input("Enter the column name to describe: ")
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
            option = input("Enter the option: ")

            if option == "-1":
                print("Going back to the previous menu...")
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
            option = input("\nEnter the option: ")

            if option == "-1":
                print("\nGoing back to the previous menu...")
                break

            try:
                option = int(option)
                if option == 1:
                    categorical_encoder.show_categorical_columns()
                elif option == 2:
                    # column_name = input("Enter the column name to perform one-hot encoding: ")
                    self.dataset=categorical_encoder.perform_one_hot_encoding()
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
            option = input("\nEnter the option: ")

            if option == "-1":
                print("\nGoing back to the previous menu....")
                break

            try:
                option = int(option)
                if option == 1:
                    column_names = input("\nEnter the column name(s) to perform normalization (comma-separated): ")
                    column_names = [col.strip() for col in column_names.split(',')]
                    self.dataset=feature_scaler.perform_normalization(column_names)
                elif option == 2:
                    column_names = input("\nEnter the column name(s) to perform standardization (comma-separated): ")
                    column_names = [col.strip() for col in column_names.split(',')]
                    self.dataset=feature_scaler.perform_standardization(column_names)
                elif option == 3:
                    feature_scaler.show_dataset()
                else:
                    print("Invalid option. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter a valid option.")

    def perform_dataset_download(self):
        if self.dataset is not None:
            download_obj = DownloadDataset(self.dataset)
            filename = input("\nEnter the file name you want to give to the dataset: ")
            if filename == "-1":
                print("Going back to the previous menu...")
            else:
                download_obj.download_dataset(filename)
        else:
            print("Error: Dataset is not loaded. Please load the dataset first using 'load_dataset' function.")


if __name__ == "__main__":
    project = Preprocess()
    project.start()
