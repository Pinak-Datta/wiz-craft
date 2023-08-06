WizCraft - CLI-Based Dataset Preprocessing Tool
===============================================

WizCraft is a cutting-edge Command Line Interface (CLI) tool developed
to simplify the process of dataset preprocessing for machine learning
tasks. It aims to provide a seamless and efficient experience for data
scientists of all levels, facilitating the preparation of data for
various machine-learning applications.

`Try the tool online here <https://replit.com/@PinakDatta/DataWiz>`__

Table of Contents
-----------------

- Features <#features>
- Getting Started <#getting-started>

   - Installation <#installation>
   - Usage <#usage>

- Tasks <#tasks>

   - Data Description <#data-description>
   - Handle Null Values <#handle-null-values>
   - Encode Categorical Values <#encode-categorical-values>
   - Feature Scaling <#feature-scaling>
   - Save Preprocessed Dataset <#save-preprocessed-dataset>

- Future Works <#future-works>

Features
--------

- Load and preprocess your dataset effortlessly through a Command Line
  Interface (CLI).
- View dataset statistics, null value counts, and perform data
  imputation.
- Encode categorical variables using one-hot encoding.
- Normalize and standardize numerical features for better model
  performance.
- Download the preprocessed dataset with your desired modifications.

Getting Started
---------------

Installation
~~~~~~~~~~~~

1. Clone this repository::

   git clone https://github.com/Pinak-Datta/wiz-craft.git
   cd wiz-craft

2. Install the required dependencies::

   pip install -r requirements.txt

Usage
~~~~~

1. To use the module, use the commands::

   from wizcraft import Wizcraft
   wz_object = Wizcraft()
   wz_object.run()

2. Follow the on-screen prompts to load your dataset, select target
   variables, and perform preprocessing tasks.

Features Available
------------------

Data Description
~~~~~~~~~~~~~~~~

1. View statistics and properties of numeric columns.
2. Explore unique values and statistics of categorical columns.
3. Display a snapshot of the dataset.

Handle Null Values
~~~~~~~~~~~~~~~~~~

1. Show NULL value counts in each column.
2. Remove specific columns or fill NULL values with mean, median, or
   mode.

Encode Categorical Values
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Identify and list categorical columns.
2. Perform one-hot encoding on categorical columns.

Feature Scaling
~~~~~~~~~~~~~~~

1. Normalize (Min-Max scaling) or standardize (Standard Scaler)


Save the Modified Dataset
~~~~~~~~~~~~~~~

1. Download the modified dataset with applied preprocessing steps.
