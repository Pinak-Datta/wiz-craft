import argparse
import sys

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


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "apply":
        parser = build_apply_parser()
        args = parser.parse_args(argv[1:])
        apply_recipe(args.csv_file, args.recipe, args.out)
        print(f"Dataset saved to {args.out}")
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
