##Libraries
import numpy as np
import pulp
import pandas as pd


def BiomassDemandSupply(demand_history,
                        distances_df,
                        year,
                        processing_capacities = 20000):

  distances = distances_df.copy()

  # Create the new row
  new_row = {x:0 for x in distances.columns}
  # Append the new row to the DataFrame
  distances = distances.append(new_row, ignore_index=True)

  overallDepotCapacity = len(distances.columns)*processing_capacities
  totalHarvestedBiomass = demand_history[f"{year}"].sum()
  dummyDemandPointCapacity = overallDepotCapacity - totalHarvestedBiomass

  sites_idx = distances.index.to_list()
  depots_idx = distances.columns.to_list()

  biomass_capacities = demand_history[f"{year}"].tolist()
  biomass_capacities.append(dummyDemandPointCapacity)
  biomass_capacities = np.array(biomass_capacities)

  forecasted_biomass = np.sum(biomass_capacities)

  # Create a Linear Programming problem
  prob = pulp.LpProblem("Biomass_Transportation", pulp.LpMinimize)

  # Create decision variables
  x = {(i, j): pulp.LpVariable(f'x_{i}_{j}', lowBound=0) for j in depots_idx for i in sites_idx}

  # Objective function: minimize transportation cost
  prob += pulp.lpSum(distances.loc[i, j] * x[i, j] for i in sites_idx for j in depots_idx)

  # Constraints
  # Harvesting sites supply constraint
  for i in sites_idx:
    prob += pulp.lpSum(x[i, j] for j in depots_idx) == biomass_capacities[i]
    #prob += pulp.lpSum(x[i, j] for j in depots_idx) >= 0.8 * biomass_capacities[i]

  #prob += pulp.lpSum(x[i, j] for i in sites_idx for j in depots_idx) >= 0.8 * forecasted_biomass

  # Depot demand constraint
  for j in depots_idx:
    prob += pulp.lpSum(x[i, j] for i in sites_idx) == processing_capacities

  # Solve the problem
  prob.solve()

  print(f"Problem Status: {prob.status}")
  print(f"Minimum Cost Value: {prob.objective.value()}")

  if prob.status == pulp.LpStatusOptimal:
    results = [pulp.value(x[i, j]) for j in depots_idx for i in sites_idx]

    result_df = pd.DataFrame({"year":year,
              "source_index":[int(i[0]) for i in x.keys()],
              "destination_index":[int(i[1]) for i in x.keys()],
               "data_type": "biomass_demand_supply",
              "value": results})

    result_df = result_df[result_df["value"].ne(0)].sort_values("source_index").reset_index(drop=True)
    result_df["value"] = result_df["value"] - 1e-05
    result_df = result_df[result_df["source_index"].ne(2418)]

    return result_df

  else:
    return None