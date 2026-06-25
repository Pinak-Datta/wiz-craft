# WizCraft Roadmap

WizCraft is being rebuilt as a beginner-friendly CLI for auditing and cleaning tabular machine-learning datasets. The goal is to make the first run delightful, then make every preprocessing step repeatable.

## Now

- Modern Python packaging with `pyproject.toml`
- A real terminal command: `wizcraft`
- Replayable preprocessing recipes
- `wizcraft apply` for replaying recipes on future CSV files
- `wizcraft doctor` for dataset health checks, column type inference, task detection, leakage warnings, and suggested recipes
- JSON and HTML exports for Doctor reports
- Core tests for imputation, encoding, scaling, recipe replay, and dataset doctor
- Cleaner dependency metadata

## Next

- Non-interactive commands for automation
- Better terminal tables and clearer validation errors
- Better README examples and example datasets

## Later

- Export a scikit-learn preprocessing pipeline
- HTML report export
- More encoders and imputers
- Example datasets and tutorial notebooks
- Plugin-style transformations for custom preprocessing steps

## Good First Issues

Good first issues should be small, testable, and useful to beginners. Examples:

- Improve an error message
- Add a test for an existing transformation
- Add an example CSV and README walkthrough
- Improve table formatting for one menu
- Add validation for a user prompt
