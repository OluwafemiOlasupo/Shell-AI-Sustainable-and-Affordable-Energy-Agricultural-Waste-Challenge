# Shell.ai Hackathon for Sustainable and Affordable Energy (Agricultural Waste Challenge)

## Problem Statement : 

To set up a biorefinery in a region, an understanding of the region’s current and future biomass produce will be required. This biomass needs to be collected and transported to intermediate depots for de-moisturisation and densification into pellets. The pellets will then need to be transported to the biorefinery for conversion to biofuel. This incurs high cost of feedstock transportation and associated GHG emissions, which will need to be minimised too.

In this hackathon, we will build digital solutions that can design and optimise this new, complex, and strategic supply chain for biorefineries of the future. 

## Project Organization
-----------------------

    ├── LICENSE
    ├── README.md        
    ├── data
    │   ├── raw                             <- Downloaded datasets
    │   │   ├── Biomass_History.csv               
    │   │   ├── Distance_Matrix.csv              
    │   │   └── sample_sbmission.csv   
    │   └── output
    │       └── Submission.csv
    ├── models                        <- Folder to contain the saved models
    ├── notebooks
    │   ├── Analysis_notebook(ShellAI).ipynb               <- Analysis Notebook
    │   ├── scripts_runner_notebook.ipynb         <- Notebook for running the script 
    │   └── complete_model_implementation.ipynb   <- Notebook for complete implementation of the project (From EDA to submission) 
    ├── reports            
    │   └── figures                     <- Generated graphics and figures
    ├── requirements.txt                <- Requirements text file
    ├── src                             <- Source code for use in this project.
    │   ├── __init__.py                 <- Makes src a Python module
    │   ├── config.py                   <- Configuration file
    │   ├── utils.py                    <- Python script contatining the necessary utilities
    │   ├── depot_locator.py            <- Configuration file
    │   ├── optimization_model.py       <- Script for linear programming.
    │   ├── refinery_locator.py            <- Script to mske prediction snd create the submission file.
    │   ├── test_constraint.py          <- Script to confirm submission if not going against any of the constraint
    │   └── visualize.py                <- Script to generate the analysis graphics.
    └── test_environment.py             <- Script to confirm the correct python environment.
