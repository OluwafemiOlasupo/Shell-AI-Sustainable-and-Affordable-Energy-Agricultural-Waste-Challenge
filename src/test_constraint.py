"""
Created on: 30/07/2023
@authors   : Sodiq, Isreal, Femi, Oba

NAME
    test_constraint.py
    
PYTHON VERSION   
    3.7.3 
    
DESCRIPTION
    Test if the submission file meets all the required constraint
    ============================================================    
    
    test_constraint.py is a python file that checks if a submission file
    meets the competition requirements.
    
INPUT
    - Submission File (pandas.DataFrame)
    
PACKAGE LIST
    Pandas
"""



# Module List
import pandas as pd
import math

class constraintsTest():
  """
  class constraintsTest()
  """

  def __init__(self, df):
    self.df = df
    self.years = [2018, 2019]
    self.yearly_depot_capacity = 20000
    self.yearly_refinery_capacity = 100000
    self.sub_columns = ['year', 'data_type', 'source_index', 'destination_index', 'value']

  def constraints_check(self):

    # Check if the input is a DataFrame
    if not isinstance(self.df, pd.DataFrame):
      print("Error: Input is not a DataFrame.")
      return False

    # Check if the DataFrame is empty
    if self.df.empty:
      print("Error: The DataFrame is empty.")
      return False

    # Check if the DataFrame contains all necessary columns
    missCol = [x for x in self.sub_columns if x not in self.df.columns]
    if len(missCol) > 0:
      print(f"Missing Columns Error: The following columns, {missCol} are missing in the submission file.")
      return False

    # Check constraint 1: All values (forecasted biomass, biomass demand-supply, pellet demand-supply
    # must be greater than or equal to zero.
    print("="*20)
    constraint1Col = ["biomass_demand_supply","biomass_forecast","pellet_demand_supply"]
    if (self.df[self.df["data_type"].isin(constraint1Col)]["value"] >= 0).all():
        print("Constraint 1 Passed Successfuly: All values are greater than or equal to zero")
    else:
        print("Constraint 1 violated: All values are not greater than or equal to zero")

    # Check constraint 2: The amount of biomass procured for processing from each harvesting site ′𝑖′
    # must be less than or equal to that site’s forecasted biomass.
    print("="*20)
    for year in self.years:
      tempDf = pd.DataFrame()
      tempDf['biomass_procured'] = self.df[self.df["data_type"].eq("biomass_demand_supply") & self.df["year"].eq(year)].groupby("source_index")["value"].sum().values
      tempDf['forecasted_biomass'] = self.df[self.df["data_type"].eq("biomass_forecast") & self.df["year"].eq(year)]["value"].values
      site_forecast_check = tempDf['biomass_procured'] <= tempDf['forecasted_biomass']

      if site_forecast_check.all():
        print(f"Constraint 2 Passed Successfuly for year {year}: Amount of biomass from each harvesting site is <= to the site’s forecasted biomass.")
      else:
        print(f"Constraint 2 violated for year {year}: Amount of biomass from each harvesting site is > to the site’s forecasted biomass.")

    # Check constraint 3: Total biomass reaching each preprocessing depot ′𝑗′ must
    # be less than or equal to its yearly processing capacity (20,000).
    print("="*20)
    for year in self.years:
      biomass_supply_check = (self.df[self.df["data_type"].eq("biomass_demand_supply") & self.df["year"].eq(year)].groupby("destination_index")["value"].sum() <= self.yearly_depot_capacity)
      if biomass_supply_check.all():
        print(f"Constraint 3 Passed Successfuly for year {year}: Total biomass reaching each depot is <= 20,000.")
      else:
        print(f"Constraint 3 violated for year {year}: Total biomass reaching each depot is > 20,000.")

    # Check constraint 4: Total pellets reaching each refinery ′𝑘′ must
    # be less than or equal to its yearly processing capacity (100,000).
    print("="*20)
    for year in self.years:
      pellets_supply_check = (self.df[self.df["data_type"].eq("pellet_demand_supply") & self.df["year"].eq(year)].groupby("destination_index")["value"].sum() <= self.yearly_refinery_capacity)
      if pellets_supply_check.all():
        print(f"Constraint 4 Passed Successfuly for year {year}: Total pellets reaching each refinery is <= 100,000.")
      else:
        print(f"Constraint 4 violated for year {year}: Total pellets reaching each refinery is > 100,000.")

    # Constraint 5: Number of depots should be less than or equal to 25.
    print("="*20)
    if (self.df["data_type"].value_counts()["depot_location"] <= 25):
        print("Constraint 5 Passed Successfuly: Number of depots is <= to 25")
    else:
        print("Constraint 5 violated: Number of depots is > than or equal to 25")

    # Constraint 6: Number of refineries should be less than or equal to 5.
    print("="*20)
    if (self.df["data_type"].value_counts()["refinery_location"] <= 5):
        print("Constraint 6 Passed Successfuly: Number of refineries is <= to 5")
    else:
        print("Constraint 6 violated: Number of refineries is > than or equal to 5")

    # Constrain 7: At least 80% of the total forecasted biomass must be processed by refineries each year
    print("="*20)
    for year in self.years:
      yearly_biomass = self.df[self.df["data_type"].eq("biomass_forecast") & self.df["year"].eq(year)]["value"].sum()
      processed_biomass = self.df[self.df["data_type"].eq("biomass_demand_supply") & self.df["year"].eq(year)]["value"].sum()
      if processed_biomass >= 0.8*yearly_biomass:
        print(f"Constraint 7 Passed Successfuly for year {year}: 80% of the total forecasted biomass was processed by refineries")
      else:
        print(f"Constraint 7 violated for year {year}: 80% of the total forecasted biomass was not processed by refineries")

    # Constrain 8: Total amount of biomass entering each preprocessing depot is equal to the total amount of pellets exiting that depot (within tolerance limit of 1e-03).
    print("="*20)
    for year in self.years:
      biomass_entering_depot = self.df[self.df["data_type"].eq("biomass_demand_supply") & self.df["year"].eq(year)]["value"].sum()
      pellete_exiting_depot = self.df[self.df["data_type"].eq("pellet_demand_supply") & self.df["year"].eq(year)]["value"].sum()

      if (math.isclose(biomass_entering_depot, pellete_exiting_depot, abs_tol = 1e-03)):
        print(f"Constraint 8 Passed Successfuly for year {year}: Biomass entering depot == Pellete exiting depot")
      else:
        print(f"Constraint 8 violated for year {year}: Biomass entering depot != Pellete exiting depot")

    #### INDEX ERROR

    # Index error 9: Harvesting site location index 𝑖𝑖 should be an integer value between 0 and 2417
    notInRange = len([x for x in self.df[self.df["data_type"].eq("biomass_forecast")]["source_index"].values.tolist() if x not in range(2418)])
    notInt = len([x for x in self.df[self.df["data_type"].eq("biomass_forecast")]["source_index"].values.tolist() if type(x) != int])
    if (notInRange or notInt):
      print("="*20)
      print(f"Index Error 9: Harvesting site location index should be an integer value between 0 and 2417")

    # Index error 10: Depot location index 𝑗𝑗 must be an integer value between 0 and 2417
    notInRange = len([x for x in self.df[self.df["data_type"].eq("depot_location")]["source_index"].values.tolist() if x not in range(2418)])
    notInt = len([x for x in self.df[self.df["data_type"].eq("depot_location")]["source_index"].values.tolist() if type(x) != int])
    if (notInRange or notInt):
      print("="*20)
      print(f"Index Error 10: Depot location index must be an integer value between 0 and 2417")

    # Index error 11: Biorefinery location index 𝑘𝑘 must be an integer value between 0 and 2417
    notInRange = len([x for x in self.df[self.df["data_type"].eq("refinery_location")]["source_index"].values.tolist() if x not in range(2418)])
    notInt = len([x for x in self.df[self.df["data_type"].eq("refinery_location")]["source_index"].values.tolist() if type(x) != int])
    if (notInRange or notInt):
      print("="*20)
      print(f"Index Error 11: Biorefinery location index must be an integer value between 0 and 2417")

    # Index error 12: : Harvesting site location index 𝑖𝑖 out of bound in biomass demand-supply matrix
    notInRange = len([x for x in self.df[self.df["data_type"].eq("biomass_demand_supply")]["source_index"].values.tolist() if x not in range(2418)])
    if (notInRange):
      print("="*20)
      print(f"Index Error 12: Harvesting site location index out of bound in biomass demand-supply matrix")

    # Index error 13: : Depot location index 𝑗𝑗 out of bound in biomass demand-supply matrix
    notInRange = len([x for x in self.df[self.df["data_type"].eq("biomass_demand_supply")]["destination_index"].values.tolist() if x not in range(2418)])
    if (notInRange):
      print("="*20)
      print(f"Index Error 13: Depot location index out of bound in biomass demand-supply matrix")

    # Index error 14: : Depot location index 𝑗𝑗 out of bound in pellet demand-supply matrix
    notInRange = len([x for x in self.df[self.df["data_type"].eq("pellet_demand_supply")]["source_index"].values.tolist() if x not in range(2418)])
    if (notInRange):
      print("="*20)
      print(f"Index Error 14: Depot location index out of bound in pellet demand-supply matrix")

    # Index error 15: : Biorefinery location index 𝑘𝑘 out of bound in pellet demand-supply matrix
    notInRange = len([x for x in self.df[self.df["data_type"].eq("pellet_demand_supply")]["destination_index"].values.tolist() if x not in range(2418)])
    if (notInRange):
      print("="*20)
      print(f"Index Error 15: Biorefinery location index out of bound in pellet demand-supply matrix")

    # Index error 16: You can only specify one value of biomass forecast per location. Multiple found.
    for year in self.years:
      uniqueIdx = self.df[self.df["data_type"].eq("biomass_forecast") & self.df["year"].eq(year)]["source_index"].value_counts().values
      if ((uniqueIdx > 1).all()):
        print("="*20)
        print(f"Index Error 16 for {year}: You can only specify one value of biomass forecast per location. Multiple found.")

    # Index error 17: You can only place one depot per location. Multiple found.
    uniqueIdx = self.df[self.df["data_type"].eq("depot_location")]["source_index"].value_counts().values
    if ((uniqueIdx > 1).any()):
      print("="*20)
      print(f"Index Error 17: You can only place one depot per location. Multiple found.")

    # Index error 18: You can only place one biorefinery per location. Multiple found.
    uniqueIdx = self.df[self.df["data_type"].eq("drefinery_location")]["source_index"].value_counts().values
    if ((uniqueIdx > 1).any()):
      print("="*20)
      print(f"Index Error 18: You can only place one biorefinery per location. Multiple found.")
