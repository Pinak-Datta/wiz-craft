# WizCraft Roadmap

WizCraft is being rebuilt as a beginner-friendly CLI for cleaning tabular machine-learning datasets. The goal is to make the first run delightful, then make every preprocessing step repeatable.

## Now

- Modern Python packaging with `pyproject.toml`
- A real terminal command: `wizcraft`
- Core tests for imputation, encoding, and scaling
- Cleaner dependency metadata

## Next

- Recipe export: save interactive preprocessing steps to JSON
- Recipe replay: apply the same cleanup steps to another CSV
- Non-interactive commands for automation
- Dataset health report for nulls, duplicates, types, cardinality, and target balance
- Better terminal tables and clearer validation errors

## Later

- Export a scikit-learn preprocessing pipeline
- HTML report export
- More encoders and imputers
- Example datasets and tutorial notebooks
- Plugin-style transformations

## Good First Issues

Good first issues should be small, testable, and useful to beginners. Examples:

- Improve an error message
- Add a test for an existing transformation
- Add an example CSV and README walkthrough
- Improve table formatting for one menu
- Add validation for a user prompt
