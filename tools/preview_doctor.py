from pathlib import Path

import pandas as pd
from rich.console import Console

from wizcraft.doctor import inspect_dataset, render_report


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_DIR = ROOT / "work" / "doctor-preview"
CSV_PATH = PREVIEW_DIR / "titanic_like.csv"
HTML_PATH = PREVIEW_DIR / "doctor-preview.html"


def create_sample_csv():
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            "PassengerId": [1, 2, 3, 4, 5, 6],
            "Age": [22, None, 26, 35, 35, 1000],
            "Sex": ["male", "female", "female", "female", "male", "male"],
            "Embarked": ["S", "C", "S", "S", "S", "Q"],
            "Cabin": [None, "C85", None, "C123", None, None],
            "Fare": [7.25, 71.28, 7.92, 53.10, 8.05, 999.00],
            "Survived": [0, 1, 1, 1, 1, 1],
        }
    ).to_csv(CSV_PATH, index=False)


def build_preview():
    create_sample_csv()
    report = inspect_dataset(CSV_PATH, target="Survived")
    console = Console(record=True, width=100)
    render_report(report, console=console)
    html = console.export_html(
        inline_styles=True,
        code_format='<pre style="font-size:14px; line-height:1.25">{code}</pre>',
    )
    html = html.replace(
        "<head>",
        "<head><title>WizCraft Dataset Doctor Preview</title>",
        1,
    )
    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"Preview written to {HTML_PATH}")


if __name__ == "__main__":
    build_preview()
