# WizCraft Examples

These small CSV files are intentionally messy so you can try WizCraft without preparing your own dataset first.

You can also create packaged copies of the samples from the CLI:

```bash
wizcraft sample
wizcraft sample titanic --out titanic.csv
wizcraft sample customers --out customers.csv
```

## Titanic Mini

Audit the sample:

```bash
wizcraft doctor examples/titanic_mini.csv --target Survived
```

Write a repeatable cleaning recipe and Markdown report:

```bash
wizcraft doctor examples/titanic_mini.csv --target Survived --write-recipe examples/titanic_mini.recipe.json --markdown examples/titanic_mini.report.md
```

Apply the recipe:

```bash
wizcraft apply examples/titanic_mini.csv --recipe examples/titanic_mini.recipe.json --out examples/titanic_mini_clean.csv
```

## Messy Customers

Audit the sample:

```bash
wizcraft doctor examples/messy_customers.csv --target churned
```

Export machine-readable, HTML, and Markdown reports:

```bash
wizcraft doctor examples/messy_customers.csv --target churned --json examples/messy_customers.report.json --html examples/messy_customers.report.html --markdown examples/messy_customers.report.md
```

Write and apply a cleaning recipe:

```bash
wizcraft doctor examples/messy_customers.csv --target churned --write-recipe examples/messy_customers.recipe.json
wizcraft apply examples/messy_customers.csv --recipe examples/messy_customers.recipe.json --out examples/messy_customers_clean.csv
```
