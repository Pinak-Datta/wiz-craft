from importlib.resources import files
from pathlib import Path


SAMPLES = {
    "titanic": {
        "filename": "titanic_mini.csv",
        "description": "Small passenger dataset with missing values, duplicates, outliers, categorical columns, and review text.",
        "target": "Survived",
    },
    "customers": {
        "filename": "messy_customers.csv",
        "description": "Customer churn dataset with IDs, dates, missing values, text feedback, outliers, and categorical columns.",
        "target": "churned",
    },
}


def list_samples():
    return [
        {"name": name, **metadata}
        for name, metadata in sorted(SAMPLES.items())
    ]


def copy_sample(name, output_path=None, overwrite=False):
    key = name.lower()
    if key not in SAMPLES:
        available = ", ".join(sorted(SAMPLES))
        raise ValueError(f"Unknown sample '{name}'. Available samples: {available}.")

    filename = SAMPLES[key]["filename"]
    destination = Path(output_path or filename)
    if destination.exists() and not overwrite:
        raise FileExistsError(
            f"{destination} already exists. Use --force to overwrite it."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    sample = files("wizcraft").joinpath("samples", filename)
    destination.write_bytes(sample.read_bytes())
    return destination

