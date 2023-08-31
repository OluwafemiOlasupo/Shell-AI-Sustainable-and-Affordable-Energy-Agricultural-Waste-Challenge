# Libraries
import math
import pandas as pd
from sklearn.cluster import KMeans

def cluster_data(df, n_clusters = 4):
  """

  """
  kmeans_kwargs = {
      "init": "random",
      "n_init": n_clusters,
      "max_iter": 300,
      "random_state": 42}

  kmeans1 = KMeans(n_clusters=n_clusters, **kmeans_kwargs)

  kmeans1.fit(df[["Longitude","Latitude"]])

  return kmeans1.predict(df[["Longitude","Latitude"]])


def haversine_distance(lat1, lon1, lat2, lon2):
    # Earth radius in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad

    a = math.sin(d_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance
    distance = earth_radius * c

    return distance


def create_train_data(df,
                      window_size):
  """


  """
  latitude = df["Latitude"]
  longitude = df["Longitude"]

  df = df[[f"201{x}" for x in range(8)]]
  year_len = df.shape[1]

  final_df = pd.DataFrame()
  test = pd.DataFrame()

  for idx in range(year_len - window_size):

    selected_dates = [f"201{idx+x}" for x in range(window_size)]
    temp_df = pd.DataFrame()
    temp_df["Latitude"] = latitude
    temp_df["Longitude"] = longitude
    temp_df[[f"year{x}" for x in range(1,window_size+1)]] = df[selected_dates]
    temp_df["Target"] = df[f"201{idx+window_size}"]

    final_df = pd.concat([final_df, temp_df]).reset_index(drop=True)

    ## Aggregate Features
  final_df["year_avg"] = final_df[[f"year{x}" for x in range(1, window_size+1)]].mean(1)
  final_df["year_std"] = final_df[[f"year{x}" for x in range(1, window_size+1)]].std(1)

  years = [f"year{x}" for x in range(1,window_size+1)]

  for index in range(len(years) -1):
    base_year = years[index]
    other_years  = years[index+1:]
    for yr_col in other_years:
      final_df[f"{yr_col}_{base_year}_change"] = (final_df[yr_col] - final_df[base_year]) / final_df[base_year]
      final_df[f"{yr_col}_{base_year}_diff"] = final_df[yr_col] - final_df[base_year]

  return final_df