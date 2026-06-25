import argparse
import json
import sys

from wizcraft.doctor import (
    inspect_dataset,
    render_report,
    report_to_dict,
    write_html_report,
    write_json_report,
    write_recipe,
)
from wizcraft.preprocess import Preprocess
from wizcraft.recipe import apply_recipe


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
        "--missing-drop-threshold",
        type=float,
        default=0.5,
        help="Missing-value rate at which a column is flagged for review instead of imputation.",
    )
    return parser


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
