import argparse
import json
import sys

from rich.console import Console
from rich.table import Table

from wizcraft.doctor import (
    inspect_dataset,
    render_report,
    report_to_dict,
    write_html_report,
    write_json_report,
    write_markdown_report,
    write_recipe,
)
from wizcraft.preprocess import Preprocess
from wizcraft.recipe import apply_recipe
from wizcraft.samples import copy_sample, list_samples


def build_parser():
    parser = argparse.ArgumentParser(
        prog="wizcraft",
        description="Interactively preprocess a tabular dataset for machine learning.",
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        help="Path to the CSV file to preprocess.",
    )
    return parser


def build_apply_parser():
    parser = argparse.ArgumentParser(
        prog="wizcraft apply",
        description="Apply a saved WizCraft preprocessing recipe to a CSV file.",
    )
    parser.add_argument("csv_file", help="Path to the CSV file to transform.")
    parser.add_argument(
        "--recipe",
        required=True,
        help="Path to a WizCraft recipe JSON file.",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Path where the transformed CSV should be saved.",
    )
    return parser


def build_doctor_parser():
    parser = argparse.ArgumentParser(
        prog="wizcraft doctor",
        description="Audit a CSV dataset and suggest preprocessing fixes.",
    )
    parser.add_argument("csv_file", help="Path to the CSV file to inspect.")
    parser.add_argument(
        "--target",
        help="Optional target column for target-aware checks.",
    )
    parser.add_argument(
        "--write-recipe",
        help="Write the suggested preprocessing recipe to this JSON file.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for stdout.",
    )
    parser.add_argument(
        "--json",
        help="Write the full doctor report to a JSON file.",
    )
    parser.add_argument(
        "--html",
        help="Write the doctor report to an HTML file.",
    )
    parser.add_argument(
        "--markdown",
        help="Write the doctor report to a Markdown file.",
    )
    parser.add_argument(
        "--missing-drop-threshold",
        type=float,
        default=0.5,
        help="Missing-value rate at which a column is flagged for review instead of imputation.",
    )
    return parser


def build_sample_parser():
    parser = argparse.ArgumentParser(
        prog="wizcraft sample",
        description="Create a sample CSV that you can inspect with WizCraft.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        help="Sample name to create. Run without a name to list samples.",
    )
    parser.add_argument(
        "--out",
        help="Output CSV path. Defaults to the sample filename.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    return parser


def render_sample_list(console=None):
    console = console or Console()
    table = Table(title="Available WizCraft Samples")
    table.add_column("Name", style="bold green")
    table.add_column("Target")
    table.add_column("Filename")
    table.add_column("Description")
    for sample in list_samples():
        table.add_row(
            sample["name"],
            sample["target"],
            sample["filename"],
            sample["description"],
        )
    console.print(table)
    console.print("[dim]Create one with: wizcraft sample titanic[/dim]")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "apply":
        parser = build_apply_parser()
        args = parser.parse_args(argv[1:])
        apply_recipe(args.csv_file, args.recipe, args.out)
        print(f"Dataset saved to {args.out}")
        return 0

    if argv and argv[0] == "doctor":
        parser = build_doctor_parser()
        args = parser.parse_args(argv[1:])
        report = inspect_dataset(
            args.csv_file,
            target=args.target,
            missing_drop_threshold=args.missing_drop_threshold,
        )
        if args.format == "json":
            print(json.dumps(report_to_dict(report), indent=2))
        else:
            render_report(report)
        if args.write_recipe:
            write_recipe(report, args.write_recipe)
            print(f"Recipe saved to {args.write_recipe}", file=sys.stderr)
        if args.json:
            write_json_report(report, args.json)
            print(f"JSON report saved to {args.json}", file=sys.stderr)
        if args.html:
            write_html_report(report, args.html)
            print(f"HTML report saved to {args.html}", file=sys.stderr)
        if args.markdown:
            write_markdown_report(report, args.markdown)
            print(f"Markdown report saved to {args.markdown}", file=sys.stderr)
        return 0

    if argv and argv[0] == "sample":
        parser = build_sample_parser()
        args = parser.parse_args(argv[1:])
        if not args.name:
            render_sample_list()
            return 0
        try:
            output = copy_sample(args.name, output_path=args.out, overwrite=args.force)
        except (FileExistsError, ValueError) as error:
            print(str(error), file=sys.stderr)
            return 2
        print(f"Sample saved to {output}")
        return 0

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        Preprocess(csv_file=args.csv_file).start()
    except KeyboardInterrupt:
        print("\nExiting WizCraft.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
