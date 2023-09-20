<p align="center">
  <img src="https://svgshare.com/i/wCo.svg" alt="wizcraft-banner" />
</p>
<p align="center">
  <a href="https://www.producthunt.com/posts/wizcraft?utm_source=badge-featured&utm_medium=badge&utm_souce=badge-wizcraft" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=410900&theme=light" alt="WizCraft - CLI&#0032;tool&#0032;that&#0032;simplifies&#0032;the&#0032;process&#0032;of&#0032;data&#0032;pre&#0045;processing | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>
</p>

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT) 

[![Downloads](https://static.pepy.tech/personalized-badge/wiz-craft?period=total&units=international_system&left_color=brightgreen&right_color=orange&left_text=Downloads)](https://pepy.tech/project/wiz-craft)

# WizCraft - CLI-Based Dataset Preprocessing Tool

WizCraft is a cutting-edge Command Line Interface (CLI) tool developed to simplify the process of dataset preprocessing for machine learning tasks. It aims to provide a seamless and efficient experience for data scientists of all levels, facilitating the preparation of data for various machine-learning applications.

**[Try the tool online here](https://replit.com/@PinakDatta/DataWiz)**

**Check out the [Contribution Guide](https://github.com/Pinak-Datta/wiz-craft/blob/main/CONTRIBUTING.md) if you want to Contribute to this project**

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
- [Future Works](#future-works)
- [Contributing to the Project](#contribute-to-the-project)



## Features

- Load and preprocess your dataset effortlessly through a Command Line Interface (CLI).
- View dataset statistics, null value counts, and perform data imputation.
- Encode categorical variables using one-hot encoding.
- Normalize and standardize numerical features for better model performance.
- Download the preprocessed dataset with your desired modifications.

## Getting Started

### Installation

1. Run the pip command:
   ```bash
   pip install wiz-craft

2. To use the module, use the commands:
    ```python
    from wizcraft.preprocess import Preprocess
    wiz_obj = Preprocess()
    wiz_obj.start()  

3. Follow the on-screen prompts to load your dataset, select target variables, and perform preprocessing tasks.

<p align="center">
  <img src="https://i.imgur.com/XFqQGrb.png" alt="wizcraft-cli_welcome" />
</p>

## Features Available

### Data Description

<p>
  <img src="https://i.imgur.com/5sPHIaR.png" alt="data_description_preview" />
</p>

1. View statistics and properties of numeric columns.
2. Explore unique values and statistics of categorical columns.
3. Display a snapshot of the dataset.

### Handle Null Values

<p>
  <img src="https://i.imgur.com/mQVG1zu.png" alt="null_data_preview" />
</p>

1. Show NULL value counts in each column.
2. Remove specific columns or fill NULL values with mean, median, or mode.

### Encode Categorical Values

<p>
  <img src="https://i.imgur.com/cgE9YU8.png" alt="one_hot_encode_preview" />
</p>

1. Identify and list categorical columns.
2. Perform one-hot encoding on categorical columns.

### Feature Scaling

<p>
  <img src="https://i.imgur.com/75JGb5X.png" alt="scaling_preview" />
</p>

1. Normalize (Min-Max scaling) or standardize (Standard Scaler) numerical columns.

### Save Preprocessed Dataset

<p>
  <img src="https://i.imgur.com/1v0Ra3s.png" alt="save_preview" />
</p>

1. Download the modified dataset with applied preprocessing steps.

## Future Works

- [ ] Undo/Redo Option for each step

- [ ] Extension for NLP tasks (like tokenization, stemming)

- [ ] Advanced Data Imputation Techniques: Adding support for advanced data imputation techniques, such as K-nearest neighbours (KNN) imputation.

- [ ] User-Friendly Interface: Improving the user interface to provide more interactive and user-friendly features, such as progress bars, error handling, and clear instructions.

- [ ] Using Curses for terminal Manipulation.

## Contributing to the Project
**Check out the [Contribution Guide](https://github.com/Pinak-Datta/wiz-craft/blob/main/CONTRIBUTING.md) if you want to contribute to this project**
