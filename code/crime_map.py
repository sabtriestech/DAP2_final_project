import geopandas as gpd
from pathlib import Path
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).parent.parent
BASE_DIR

os.chdir(BASE_DIR)
data_w_geo= gpd.read_file(os.path.join("data\derived_data\Full Data with Geography.gpkg"))

county_map = gpd.read_file(os.path.join('data\Shapefiles\County\co99_d00.shp'))
#drop Alaska and Hawaii
county_map = county_map[county_map['STATE'] != '02']
county_map = county_map[county_map['STATE'] != '15']

#want to collapse to single row per county
data_grouped_geo = data_w_geo[
    (data_w_geo["Ownership"] == "Private") &
    (data_w_geo["Industry"] == "Total, all industries")]

data_grouped_geo = data_grouped_geo[data_grouped_geo["state_name"]!="Hawaii"]

#want to winsorize property crime to display better
pctile95 = data_grouped_geo['Property crime_rate'].quantile(0.95)
data_grouped_geo["Property crime_rate_winsor"] = np.where(data_grouped_geo["Property crime_rate"] > pctile95, 
                                                     pctile95, 
                                                     data_grouped_geo["Property crime_rate"]) 

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

county_map.plot(
    color='lightgrey',   
    ax=ax)

data_grouped_geo.plot(
    column='Property crime_rate_winsor',              
    linewidth=0.2,           
    edgecolor='0.5',          
    legend=True,              
    ax=ax,
    zorder=2,
    cmap='magma',
    )

cbar_ax = fig.axes[-1]
cbar_ax.set_title('Property Crime Rate\n(per 1,000 residents)', fontsize=10)
ax.set_position([0.03, 0.08, 0.82, 0.85])
cbar_ax.set_position([0.87, 0.25, 0.02, 0.5])

ax.set_title('County-Level Property Crime Rates', fontsize=24)
ax.axis('off')  

ax.set_axis_off()
plt.show()

pctile95 = data_grouped_geo['Violent crime_rate'].quantile(0.95)
data_grouped_geo["Violent crime_rate_winsor"] = np.where(data_grouped_geo["Violent crime_rate"] > pctile95, 
                                                     pctile95, 
                                                     data_grouped_geo["Violent crime_rate"]) 

# now for violent crime
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

county_map.plot(
    color='lightgrey',   
    ax=ax)

data_grouped_geo.plot(
    column='Violent crime_rate_winsor',              
    linewidth=0.2,           
    edgecolor='0.5',          
    legend=True,              
    ax=ax,
    zorder=2,
    cmap='magma',
    )

cbar_ax = fig.axes[-1]
cbar_ax.set_title('Violent Crime Rate\n(per 1,000 residents)', fontsize=10)
ax.set_position([0.03, 0.08, 0.82, 0.85])
cbar_ax.set_position([0.87, 0.25, 0.02, 0.5])

ax.set_title('County-Level Violent Crime Rates', fontsize=24)
ax.axis('off')  

ax.set_axis_off()
plt.show()










