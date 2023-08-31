## Libraries
import pulp
import json
import numpy as np
import pandas as pd
from visualize import plot_map

def RefineryLocator(demand_history,
                   depots_location,
                   distance_matrix,
                   years,
                   depot_apacity = 20000,
                   refinery_apacity = 100000):
  
    ### Year with the maximum total biomass harvest
    years_total_biomass = demand_history[years].sum().to_dict()
    year = max(years_total_biomass, key=years_total_biomass.get)

    demand_history["locationMap"] = demand_history["Latitude"].astype(str) + "_" + demand_history["Longitude"].astype(str)
    latlong_idx = {y:x for (x,y) in demand_history["locationMap"].to_dict().items()}

    depots_location["locationMap"] = depots_location["Latitude"].astype(str) + "_" + depots_location["Longitude"].astype(str)
    depots_location["loc_idx"] = depots_location["locationMap"].map(latlong_idx)

    rows_idx = depots_location["loc_idx"].values
    N = distance_matrix.iloc[rows_idx, :].columns.to_list()  # Possible refinery locations
    M = distance_matrix.iloc[rows_idx, :].index.to_list()  # Depots points
    d = distance_matrix.iloc[rows_idx, :].to_dict()         # Distance matrix

    thresh = int(refinery_apacity / depot_apacity)  # Threshold (Number of maximum depots that can be served by a refinery)

    p = int(np.ceil(len(M) / thresh)) # Number of facilities to locate

    # Create a PuLP minimization problem
    prob = pulp.LpProblem("P_Median_Problem", pulp.LpMinimize)
    
    # Create binary variables x[i][j] and y[i]
    x = {(i, j): pulp.LpVariable(f'x_{i}_{j}', cat=pulp.LpBinary) for i in N for j in M}
    y = {i: pulp.LpVariable(f'y_{i}', cat=pulp.LpBinary) for i in N}
    
    # Objective function: minimize total cost
    prob += pulp.lpSum(d[i][j] * x[i, j] for i in N for j in M)
    
    # Constraints
    # Each demand point must be served by exactly one facility
    for j in M:
        prob += pulp.lpSum(x[i, j] for i in N) == 1

    # Each facility point must serve by exactly one facility
    for i in N:
        prob += pulp.lpSum(x[i, j] for j in M) <= thresh 
    
    # Number of open facilities must be p
    prob += pulp.lpSum(y[i] for i in N) == p
    
    # If a facility is open, it must serve the associated demand points
    for i in N:
        for j in M:
            prob += x[i, j] <= y[i]
    
    # Solve the problem
    prob.solve()
    
    # Extract the solution
    solution = {
        i: {
            j: x[i, j].varValue for j in M
        } for i in N
    }
    
    open_facilities = [i for i in N if y[i].varValue == 1]

    idx_latlong = {key:value for (value,key) in latlong_idx.items()}

    refinery_location = pd.DataFrame()
    refinery_location["source_index"] = [int(x) for x in open_facilities]
    refinery_location["Latitude"] = refinery_location["source_index"].apply(lambda x: float(idx_latlong[x].split("_")[0]))
    refinery_location["Longitude"] = refinery_location["source_index"].apply(lambda x: float(idx_latlong[x].split("_")[1]))
    refinery_location["year"] = int(f"{years[0]}{years[1]}")
    refinery_location["data_type"] = "refinery_location"
    refinery_location["destination_index"] = 0
    refinery_location["value"] = 0

    print("Solution:")
    solDict = {}
    for i in open_facilities:
        print(f"Facility {i} - Demand Points: {', '.join(str(j) for j in M if solution[i][j] == 1)}")
        solDict[i] = [j for j in M if solution[i][j] == 1]

    print("Open Facilities:", open_facilities)

    df_dict = {"source_index":[],
           "destination_index":[],
           "data_type":"pellet_demand_supply"}

    for key, val in solDict.items():
      df_dict["source_index"] = [*df_dict["source_index"], *val]
      df_dict["destination_index"] = [*df_dict["destination_index"], *[int(key)]*len(val)]
    

    plot_map(df = demand_history,
        year = year,
        depot_data = depots_location,
        refinery_data = refinery_location,
        cluster_col = "Clusters")
        
    return refinery_location, pd.DataFrame(df_dict)