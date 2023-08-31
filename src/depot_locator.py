## Libraries
import json
import numpy as np
import pandas as pd
from visualize import plot_map
from utils import cluster_data, haversine_distance

def center_of_gravity_method(df):
  """
  The COG is the weighted average of the latitude, longitude, and demand,
  where each coordinate is multiplied by the corresponding demand and then
  divided by the sum of the demands.

  It locates just one facility in a location

  Parameters:
    df (pd.DataFrame): A dataframe containing the biomass demand data for different years and
                      the harvesting locations latitude and longitude for one cluster of the whole location.
  Example:
      >>> df         :| 	|  Latitude	 | Longitude	|  2010	     | 2011	     |  ...  | 2014	      |
                      | 0	|  24.66818	 | 71.33144	  |  8.475744	 | 8.868568	 |  ...  | 9.202181	  |
                      | 1	|  24.66818	 | 71.41106	  |  24.029778 | 28.551348 |  ...  | 25.866415	|
                        .        .            .           .            .         .         .
                        .        .            .           .            .         .         .
                        .        .            .           .            .         .         .

                      |n-1|  24.66818	 | 71.49069	  |  44.831635 | 66.111168 |  ...  | 56.982258	|	
                      | n	|  24.66818	 | 71.57031	  |  59.974419 | 80.821304 |  ...  | 78.956543	|
      >>> center_of_gravity_method(df)
      Output: [24.66818, 71.33144]
  """

  data = df[["Latitude", "Longitude" , "2017"]].values

  # Calculate the Center of Gravity (COG) for the entire dataset
  cog_latitude = np.sum(data[:, 0] * data[:, 2]) / np.sum(data[:, 2])
  cog_longitude = np.sum(data[:, 1] * data[:, 2]) / np.sum(data[:, 2])

  grid_distance = {}
  for x in df[["Latitude","Longitude"]].values:
    lat, lon = x[0], x[1]
    key = str(lat) + "_" + str(lon)
    value = haversine_distance(cog_latitude, cog_longitude, lat, lon)
    grid_distance[key] = value

  closet_grid = min(grid_distance, key=grid_distance.get)
  fac_lat, fac_lon = closet_grid.split("_")
  facility_location = [float(fac_lat), float(fac_lon)]

  return facility_location


def DepotLocator(df,
                    years = [],
                    facility_capacity = 20000,
                    facility_type = "depots"):
  """
  Optimal facility location using clustering and center of gravity method.

  Parameters:
    df (pd.DataFrame): A dataframe containing the biomass demand data for different years and
                      the harvesting locations latitude and longitude.

    years (array): Array of years whose biomass demand data will be used to determine the needed
                    number of facilities.

    facility_capacity (int): The capacity of each facilities.

    facility_type (str): The type of facilities to be located.

  Returns:
    dataframe: A dataframe whose rows represent the optimal locations (Latitude and Longitude) of
                the facilities.

  Example:
      >>> df         :| 	|  Latitude	 | Longitude	|  2010	     | 2011	     |  ...  | 2014	      |
                      | 0	|  24.66818	 | 71.33144	  |  8.475744	 | 8.868568	 |  ...  | 9.202181	  |
                      | 1	|  24.66818	 | 71.41106	  |  24.029778 | 28.551348 |  ...  | 25.866415	|
                        .        .            .           .            .         .         .
                        .        .            .           .            .         .         .
                        .        .            .           .            .         .         .

                      |n-1|  24.66818	 | 71.49069	  |  44.831635 | 66.111168 |  ...  | 56.982258	|	
                      | n	|  24.66818	 | 71.57031	  |  59.974419 | 80.821304 |  ...  | 78.956543	|
      >>> years = [2011, 2012]
      >>> facility_capacity = 20000
      >>> facility_type = "depots"
      >>> FacilityLocator(df, years, facility_capacity, facility_type)
      Output:
            | 	|  Latitude	 | Longitude	|
            | 0	|  24.66818	 | 71.33144	  | 
            | 1	|  24.66818	 | 71.41106	  | 
            | 2	|  24.66818	 | 71.49069	  |
  """
  import math
  import json

  ### Year with the maximum total biomass harvest
  years_total_biomass = df[years].sum().to_dict()
  year = max(years_total_biomass, key=years_total_biomass.get)

  ## Total number of needed Facilities
  total_facility_needed = math.ceil(years_total_biomass[year] / facility_capacity)

  print("Total Needed Facilities : ", total_facility_needed)

  ## Divide the whole location into different clusters
  df["Clusters"] = cluster_data(df = df,
                                n_clusters = 4)

  needed_facilities = (df.groupby("Clusters")[f"{year}"].agg("sum") / facility_capacity).to_dict()

  print("Needed Facilities :", json.dumps(needed_facilities, indent=4))

  assigned_facilities = round(df.groupby("Clusters")[f"{year}"].agg("sum") / facility_capacity).to_dict()

  print("Assigned Facilities :", json.dumps(assigned_facilities, indent=4))

  total_assigned_facilities = sum(assigned_facilities.values())

  if total_assigned_facilities > total_facility_needed:
    print(f"The total assigned {facility_type} is greater than the needed facilities by {total_assigned_facilities - total_facility_needed} {facility_type}")

  elif total_assigned_facilities < total_facility_needed:
    print(f"The total assigned {facility_type} is lesser than the needed facilities by {total_facility_needed - total_assigned_facilities} {facility_type}")

    # Subtract the values of dict2 from dict1
    result_dict = {key: needed_facilities[key] - assigned_facilities[key] if needed_facilities[key] - assigned_facilities[key] > 0 else 0  for key in assigned_facilities}
    print("Remnant Facilities :", json.dumps(result_dict, indent=4))

  else:
    pass

  ## Optimally Locate the Facilities using center of gravity method
  facilities_locations = []

  for cluster, n_cluster in assigned_facilities.items():
    temp_df = df[df["Clusters"].eq(cluster)].reset_index(drop=True)
    temp_df["new_Clusters"] = cluster_data(df = temp_df,
                                  n_clusters = int(n_cluster))

    for new_cluster in range(int(n_cluster)):
      new_df = temp_df[temp_df["new_Clusters"].eq(new_cluster)].reset_index(drop=True)
      facility_location = center_of_gravity_method(new_df)
      facilities_locations.append(facility_location)

  if total_assigned_facilities < total_facility_needed:
    result_dict = {key: needed_facilities[key] - assigned_facilities[key] if needed_facilities[key] - assigned_facilities[key] > 0 else 0  for key in assigned_facilities}
    filtered_keys = [key for key, value in result_dict.items() if value > 0]

    extra_facility_df = df[df["Clusters"].isin(filtered_keys)].reset_index(drop=True)
    extra_facilities_needed = total_facility_needed - total_assigned_facilities
    print(f"extra_facilities_needed: {extra_facilities_needed}")

    if extra_facilities_needed > 1:

      extra_facility_df["new_Clusters"] = cluster_data(df = extra_facility_df,
                                  n_clusters = int(extra_facilities_needed))

      for new_cluster_ in range(int(extra_facilities_needed)):
        new_df = extra_facility_df[extra_facility_df["new_Clusters"].eq(new_cluster_)].reset_index(drop=True)
        facility_location = center_of_gravity_method(new_df)
        print(f"Extra Facilities: {facility_location}")
        facilities_locations.append(facility_location)

    else:
      facility_location = center_of_gravity_method(extra_facility_df)
      print(f"Extra Facilities: {facility_location}")
      facilities_locations.append(facility_location)

  facility_data = pd.DataFrame(facilities_locations, columns = ["Latitude","Longitude"])
  facility_data["year"] = int(f"{years[0]}{years[1]}")
  facility_data["data_type"] = "depot_location"
  facility_data["destination_index"] = 0
  facility_data["value"] = 0

  latlong_idx = {y:x for (x,y) in (df["Latitude"].astype(str) + "_" + df["Longitude"].astype(str)).to_dict().items()}

  facility_data["source_index"] = (facility_data["Latitude"].astype(str) + "_" + facility_data["Longitude"].astype(str)).map(latlong_idx)


  plot_map(df = df,
          year = year,
          depot_data = facility_data,
          refinery_data = None,
          cluster_col = "Clusters")

  return facility_data