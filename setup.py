from setuptools import setup, find_packages

with open('Readme.md', 'r') as file_handler:
    long_description = file_handler.read()

VERSION = '0.0.2',
DESCRIPTION = 'A CLI-based dataset preprocessing tool for machine learning tasks. Features include data exploration, ' \
              'null value handling, one-hot encoding, and feature scaling, and download the modified dataset ' \
              'effortlessly. '
setup(
    name='wiz-craft',
    version='0.0.1',
    author_email='pinakdatta2002@gmail.com',
    author='Pinak Datta',
    description='A CLI-based dataset preprocessing tool for machine learning tasks. Features include data '
                'exploration, null value handling, one-hot encoding, and feature scaling, and download the modified '
                'dataset effortlessly.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
        'pandoc'
    ],
    keywords=['Dataset preprocessing', 'Data cleaning', 'Machine learning', 'Data analysis', 'Data manipulation',
              'Data preparation', 'Data engineering', 'CLI tool', 'Command Line Interface', 'Data science',
              'Feature scaling', 'One-hot encoding', 'Data imputation', 'Null value handling', 'Data exploration',
              'Data visualization', 'Python library', 'Data transformation', 'Data processing', 'DataWiz', 'Wizcraft',
              'wiz-craft', 'WizCraft'
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ]
)
