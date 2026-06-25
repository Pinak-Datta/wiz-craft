<p align="center">
  <img src="https://svgshare.com/i/wCo.svg" alt="wizcraft-banner" />
  

</p>
<p align="center">
  <a href="https://www.producthunt.com/posts/wizcraft?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-wizcraft" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=410900&theme=light" alt="WizCraft - CLI&#0032;tool&#0032;that&#0032;simplifies&#0032;the&#0032;process&#0032;of&#0032;data&#0032;pre&#0045;processing | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
</p>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT) 
[![CI](https://github.com/Pinak-Datta/wiz-craft/actions/workflows/ci.yml/badge.svg)](https://github.com/Pinak-Datta/wiz-craft/actions/workflows/ci.yml)

[![Downloads](https://static.pepy.tech/personalized-badge/wiz-craft?period=total&units=international_system&left_color=brightgreen&right_color=orange&left_text=Downloads)](https://pepy.tech/project/wiz-craft)

![PyPI - Version](https://img.shields.io/pypi/v/wiz-craft)


# WizCraft - CLI-Based Dataset Preprocessing Tool

WizCraft is a beginner-friendly Command Line Interface (CLI) tool for preparing tabular datasets for machine learning. It helps you inspect a CSV, handle missing values, encode categorical columns, scale numeric features, save a cleaned dataset, and export replayable preprocessing recipes.

**[Try the tool online here](https://replit.com/@PinakDatta/DataWiz)**

**Check out the [Contribution Guide](https://github.com/Pinak-Datta/wiz-craft/blob/main/CONTRIBUTING.md) if you want to contribute to this project**

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [Tasks](#tasks)
  - [Data Description](#data-description)
  - [Handle Null Values](#handle-null-values)
  - [Encode Categorical Values](#encode-categorical-values)
  - [Feature Scaling](#feature-scaling)
  - [Save Preprocessed Dataset](#save-preprocessed-dataset)
- [Replayable Recipes](#replayable-recipes)
- [Roadmap](#roadmap)
- [Contributing to the Project](#contribute-to-the-project)



## Features

- Load and preprocess your dataset effortlessly through a Command Line Interface (CLI).
- View dataset statistics, null value counts, and perform data imputation.
- Encode categorical variables using one-hot encoding.
- Normalize and standardize numerical features for better model performance.
- Download the preprocessed dataset with your desired modifications.
- Save preprocessing recipes and replay them on future CSV files.

## Getting Started

### Installation

Install WizCraft from PyPI:

```bash
pip install wiz-craft
```

Start the interactive CLI with a CSV file:

```bash
wizcraft dataset.csv
```

You can also launch WizCraft and choose a CSV from the current directory:

```bash
wizcraft
```

WizCraft can still be used from Python:

```python
from wizcraft.preprocess import Preprocess

wiz_obj = Preprocess(csv_file="dataset.csv")
wiz_obj.start()
```

Follow the on-screen prompts to select the target variable and perform preprocessing tasks.

Replay a saved recipe on another CSV:

```bash
wizcraft apply new-data.csv --recipe cleaned.recipe.json --out new-data-clean.csv
```

<p align="center">
  <img src="https://i.imgur.com/jYLwMN7.png" alt="wizcraft-cli_welcome" width = "600" height = "300" />
</p>

## Features Available

### Data Description

<p>
  <img src="https://i.imgur.com/2CUMMoX.png" alt="data_description_preview" />
</p>

1. View statistics and properties of numeric columns.
2. Explore unique values and statistics of categorical columns.
3. Display a snapshot of the dataset.

### Handle Null Values

<p>
  <img src="https://i.imgur.com/JlkyQl5.png" alt="null_data_preview" />
</p>

1. Show NULL value counts in each column.
2. Remove specific columns or fill NULL values with mean, median, mode, or K-nearest neighbors.

### Encode Categorical Values

<p>
  <img src="https://i.imgur.com/0gEfhpi.png" alt="one_hot_encode_preview" />
</p>

1. Identify and list categorical columns.
2. Perform one-hot encoding on categorical columns.

### Feature Scaling

<p>
  <img src="https://i.imgur.com/kfpoXeG.png" alt="scaling_preview" />
</p>

1. Normalize (Min-Max scaling) or standardize (Standard Scaler) numerical columns.

### Save Preprocessed Dataset

<p>
  <img src="https://i.imgur.com/1XywkGQ.png" alt="save_preview" />
</p>

1. Download the modified dataset with applied preprocessing steps.
2. Save a replayable `.recipe.json` file for the same preprocessing flow.

## Replayable Recipes

WizCraft can now save the preprocessing steps you perform interactively. A recipe is a small JSON file that can be applied again later:

```bash
wizcraft apply raw-data.csv --recipe cleaned.recipe.json --out cleaned-data.csv
```

Recipes currently support:

- Removing columns
- Filling null values with mean, median, mode, or K-nearest neighbors
- One-hot encoding categorical columns
- Normalizing or standardizing numeric columns

## Roadmap

WizCraft is being rebuilt around two ideas: a friendly first-time CLI and repeatable preprocessing recipes.

Current priorities:

- Non-interactive commands for automation and notebooks.
- Dataset health reports for nulls, duplicates, types, cardinality, and target balance.
- Exportable scikit-learn preprocessing pipelines.
- Cleaner terminal tables, validation, and error messages.
- Example datasets, tutorials, and good first issues for new contributors.

See [ROADMAP.md](ROADMAP.md) for the full direction.

## Contributing to the Project
**Check out the [Contribution Guide](https://github.com/Pinak-Datta/wiz-craft/blob/main/CONTRIBUTING.md) if you want to contribute to this project**
