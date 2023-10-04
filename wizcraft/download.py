# download.py

import pandas as pd


class DownloadDataset:
    def __init__(self, dataset):
        self.dataset = dataset

    def download_dataset(self, filename):
        try:
            self.dataset.to_csv(filename+".csv", index=False)
            print(f"\nDataset saved successfully as '{filename}'....!!!")
        except Exception as e:
            print(f"Error: Failed to download the dataset. {e}")


if __name__ == "__main__":
    # For testing the DownloadDataset class
    df = pd.DataFrame({'Column1': [1, 2, 3, 4, 5],
                       'Column2': [10, 20, 30, 40, 50],
                       'Column3': [100, 200, 300, 400, 500]})

    download_obj = DownloadDataset(df)
    download_obj.download_dataset('preprocessed_dataset.csv')
