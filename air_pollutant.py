import folium
from folium.plugins import HeatMap, HeatMapWithTime
import pandas as pd
import numpy as np

# Create data frame for CO pollutant
df = pd.read_csv(r"D:\GIS & Geospatial Analysis with Python Geopandas and Folium\Projects\AirQualityIndex\CO.csv")

# Convert the date colomn type from object to date and create a week column from it
df["Date"] = pd.to_datetime(df["Date"])
df["Week"] = df["Date"].dt.isocalendar().week

# Create a variable of mean AQI based on the site name and mean of the AQI of each week
weekly_mean_co = df.groupby(["Local Site Name", "Week"]).agg({
    "Site Latitude": "first",
    "Site Longitude": "first",
    "Daily AQI Value": lambda x: np.mean(x)
}).reset_index()

# Print the list to see the data
'''print("Weekly average of CO pollutant in each monitor site!")
for location in weekly_mean_co["Local Site Name"].unique():
    location_site = weekly_mean_co[weekly_mean_co["Local Site Name"] == location]
    print(f"Site Location: {location}")
    for index, row in location_site.iterrows():
        print(f"Week {row['Week']}, Average CO amount is {row['Daily AQI Value']:.2f}.")
    print("\n")
'''

# Data Visulization
# Create a list to store the coordinates
df_week_list = []
for week in range(1, 32):
    weekly_data = weekly_mean_co[weekly_mean_co["Week"] == week][["Site Latitude", "Site Longitude", "Daily AQI Value"]]
    df_week_list.append(weekly_data.values.tolist())
    
base_map = folium.Map(location=[34.0549, -118.2426], zoom_start=11)
co_heatmap = HeatMapWithTime(df_week_list, name="CO Heatmap",radius=150, gradient={0.05: "blue", 0.5: "green", 0.75: "yellow", 1: "red"},
                min_opacity=0.5,
                max_opacity=0.8, use_local_extrema=True).add_to(base_map)
base_map.save("Weekly_CO_Value_HeatMap.html")
base_map