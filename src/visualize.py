"""
Created on: 
@author   : 

NAME
  visualize.py
    
DESCRIPTION
    Visualizes Longitude, Latitude and Biomass demand data
    ============================================================    
    
PACKAGE LIST
  pandas
  matplotlib
"""

## Libraries
import pandas as pd
import matplotlib.pyplot as plt

def plot_map(df,
             year,
             depot_data = None,
             refinery_data = None,
             cluster_col = None):
  
  """
  Plotting biomass harvesting points and depot points.

  This function takes a DataFrame containing information about biomass harvesting points
  and depot points and generates a plot to visualize their locations on a map.

  Parameters:
      dataframe (pd.DataFrame): A pandas DataFrame containing the following columns:
                                  - 'Latitude': Latitude values of the points.
                                  - 'Longitude': Longitude values of the points.
                                  - Yearly Biomass demand
  Returns:
    None
  """
  title = "Harvesting, "
  plt.figure(figsize = (50,30))

  colorList = [
      'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'navy', 'purple', 'teal', 'lime', 'aqua',
      'fuchsia', 'olive', 'maroon', 'silver', 'gray', 'lightgray', 'darkgray', 'coral']

  if cluster_col:
    n_clusters = df[cluster_col].unique()
    for cluster in n_clusters:
      DemandSize = df[df[cluster_col].eq(cluster)][f"{year}"]
      plt.scatter(df[df[cluster_col].eq(cluster)]["Longitude"], df[df[cluster_col].eq(cluster)]["Latitude"],
                  label = f"Harvesting Points cluster {cluster}", marker ="*", color = colorList[cluster], s = DemandSize)
  else:
    DemandSize = df[f"{year}"]
    plt.scatter(df["Longitude"], df["Latitude"], label = f"Harvesting Points", marker ="*", 
                color = "b", s = DemandSize)
    
  if isinstance(depot_data, pd.DataFrame):
    plt.scatter(depot_data["Longitude"], depot_data["Latitude"], label = "Depots Points", marker ="s",color = "green", s = 1000)
    title += "Depots, "

  if isinstance(refinery_data, pd.DataFrame):
    plt.scatter(refinery_data["Longitude"], refinery_data["Latitude"], label = "Refinery Points", marker ="o",color = "red", s = 1500)
    title += "Rifineries, "

  title += "Locations"
  plt.legend()
  plt.title(title, fontsize = 35)
  plt.xlabel("Longitude", fontsize = 35)
  plt.ylabel("Latitude", fontsize = 35)

  plt.show()