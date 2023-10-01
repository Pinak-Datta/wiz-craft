# download.py

import pandas as pd
from wizcraft.io import Output


class DownloadDataset:
    def __init__(self, dataset):
        self.dataset = dataset  # .copy()
        self.output = Output()

    def download_dataset(self, filename):
        try:
            self.dataset.to_csv(filename + ".csv", index=False)
            self.output.c_print(
                f"\nDataset saved successfully as '{filename}'", code="success"
            )
        except Exception as e:
            self.output.c_print(
                f"Error: Failed to download the dataset. {e}", code="danger"
            )


if __name__ == "__main__":
    # For testing the DownloadDataset class
    df = pd.DataFrame(
        {
            "Column1": [1, 2, 3, 4, 5],
            "Column2": [10, 20, 30, 40, 50],
            "Column3": [100, 200, 300, 400, 500],
        }
    )

    download_obj = DownloadDataset(df)
    download_obj.download_dataset("preprocessed_dataset.csv")
