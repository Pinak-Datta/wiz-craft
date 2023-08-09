from setuptools import setup, find_packages

with open('Readme.md', 'r') as file_handler:
    long_description = file_handler.read()

DESCRIPTION = 'A CLI-based dataset preprocessing tool for machine learning tasks. Features include data exploration, ' \
              'null value handling, one-hot encoding, and feature scaling, and download the modified dataset ' \
              'effortlessly. '
setup(
    name='wiz-craft',
    version='1.0.2',
    url='https://github.com/Pinak-Datta/wiz-craft',
    author_email='pinakdatta2002@gmail.com',
    author='Pinak Datta',
    license='OSI Approved :: MIT License',
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
    keywords=['Dataset preprocessing', 'Data cleaning', 'Machine learning', 'Data manipulation',
              'Data preparation', 'Data engineering', 'Feature scaling', 'One-hot encoding', 'Data imputation', 'Null value handling', 'Data exploration',
              'Data processing', 'wizcraft',
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
