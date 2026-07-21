# WizCraft Launch Checklist

Use this checklist when publishing a feature release and promoting it.

## Release 1.4.0 Notes

~~~markdown
## What's new

- Added `wizcraft sample` for creating bundled demo CSV files.
- Added sample datasets for Titanic-style survival modeling and customer churn.
- Added `wizcraft doctor --markdown report.md` for shareable Markdown dataset audits.
- Improved Dataset Doctor recipe suggestions so ID-like columns are not also treated as categorical columns.
- Updated README with a 60-second quickstart and clearer positioning.

## Try it

```bash
pip install --upgrade wiz-craft
wizcraft sample titanic --out titanic.csv
wizcraft doctor titanic.csv --target Survived --write-recipe titanic.recipe.json --markdown titanic-report.md
wizcraft apply titanic.csv --recipe titanic.recipe.json --out titanic-clean.csv
```

## Verification

- `pytest -q` -> passed
- `python -m build` -> passed
- `twine check dist/*` -> passed
~~~

## Short Launch Post

```text
I just released WizCraft 1.4.0.

WizCraft is a beginner-friendly Python CLI for auditing messy CSV files before machine-learning modeling.

New in this release:
- `wizcraft sample` to create demo datasets instantly
- Markdown Dataset Doctor reports
- repeatable cleaning recipes
- better ID/text/categorical detection

Try it:
pip install --upgrade wiz-craft
wizcraft sample titanic --out titanic.csv
wizcraft doctor titanic.csv --target Survived --markdown report.md

GitHub: https://github.com/Pinak-Datta/wiz-craft
PyPI: https://pypi.org/project/wiz-craft/
```

## Where To Share

- LinkedIn
- X/Twitter
- Reddit: `r/Python`, `r/learnpython`, `r/datascience`
- Dev.to
- Hashnode
- Medium
- Product Hunt update
- GitHub Discussions

## Follow-Up Issues To Open

- `feature: export Dataset Doctor recipes as scikit-learn ColumnTransformer`
- `feature: add wizcraft doctor --fix for safe automatic cleaning`
- `feature: add more sample datasets`
- `docs: add Titanic walkthrough`
- `docs: add customer churn walkthrough`
- `good first issue: improve sample dataset descriptions`
- `good first issue: add screenshots for sample and doctor commands`
