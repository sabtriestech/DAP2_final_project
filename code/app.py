import streamlit as st
import pandas as pd
import altair as alt
import geopandas as gpd
from os.path import join
import os
import numpy as np
import matplotlib.cm as cm
import pydeck as pdk
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.pyplot as mpld3
import streamlit.components.v1 as components

import warnings
warnings.filterwarnings('ignore')
alt.renderers.enable("png")
alt.data_transformers.disable_max_rows()

BASE_DIR = Path(__file__).parent.parent


# improve graph resolution
import tempfile
from IPython.display import SVG, display, Image
import vl_convert as vlc

def display_altair_png(chart, scale=2):
    """
    Render an Altair chart to a PNG and display it inline.

    Parameters
    ----------
    chart : altair.Chart
        Altair chart object to render.
    scale : int, optional
        Resolution scaling factor for the PNG (default = 2). Use scale=2 for standard slides. Use scale = 3–4 for dense figures or PDF exports.
    """
    png_bytes = vlc.vegalite_to_png(chart.to_dict(), scale=scale)

    # Write to a temporary PNG file and display
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        tmp.write(png_bytes)
        tmp.flush()
        display(Image(filename=tmp.name))


st.set_page_config(page_title='Economic Mobility, Wages, and Crime')
st.title('Economic Mobility, Wages, and Crime')

def intro():
    import streamlit as st
    st.markdown('This dashboard allows you to explore economic mobility data and its ties to other socioeconomic indicators. To begin, select an indicator of choice')
intro()

st.markdown("### Filters")
# Type of County
all = st.checkbox("All", value=True)
under_50 = st.checkbox("Show only >50% Mobility for 25th Percentile", value=False)
over_50 = st.checkbox("Show Only <50% Mobility for 25th Percentile", value=False)

variable_choice = st.selectbox(
    "Select a Variable",
    options= ["Mobility for 25th percentile","Mobility for 75th percentile", "Violent Crime", "Property Crime", "HHI"]
)

#load and clean data
@st.cache_data
def load_data():
    df = gpd.read_file(os.path.join(BASE_DIR,"data/derived_data/Full Data with Geography.gpkg"))
    county_data = gpd.read_file(os.path.join(BASE_DIR,'data/Shapefiles/County/co99_d00.shp'))
    county_data = county_data[county_data['STATE'] != '02']
    county_data = county_data[county_data['STATE'] != '15']
    df = df[df['STATE'] != '15']
    df = df[
    (df["Ownership"] == "Private") &
    (df["Industry"] == "Total, all industries")]
    pctile95 = df['Property crime_rate'].quantile(0.95)
    df["Property crime_rate_winsor"] = np.where(df["Property crime_rate"] > pctile95, 
                                                     pctile95, 
                                                     df["Property crime_rate"]) 
    pctile95v = df['Violent crime_rate'].quantile(0.95)
    df["Violent crime_rate_winsor"] = np.where(df["Violent crime_rate"] > pctile95v, 
                                                     pctile95v, 
                                                     df["Violent crime_rate"]) 
    return df, county_data

df, county_data = load_data()

if under_50:
    df = df[df['kr26_p25_coef'] <= 0]
elif over_50:
    df = df[df['kr26_p25_coef'] >= 0]
else:
    df = df

sample_df = df

#dictionary for selected columns:
selected_column = {'Mobility for 25th percentile':'kr26_p25_coef',
                   'Mobility for 75th percentile': 'kr26_p75_coef',
                    'Property Crime': 'Property crime_rate_winsor',
                    'Violent Crime':'Violent crime_rate_winsor'}

variable_column = selected_column[variable_choice]

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

county_data.plot(
    color='lightgrey',   
    ax=ax)

sample_df.plot(
    column=variable_column,              
    linewidth=0.2,           
    edgecolor='0.5',          
    legend=True,              
    ax=ax,
    zorder=2,
    cmap='magma',
    )

cbar_ax = fig.axes[-1]
cbar_ax.set_title(f'{variable_choice}', fontsize=10)
ax.set_position([0.03, 0.08, 0.82, 0.85])
cbar_ax.set_position([0.87, 0.25, 0.02, 0.5])

ax.set_title(f'County-Level {variable_choice}', fontsize=24)
ax.axis('off')  

ax.set_axis_off()
st.pyplot(fig) 

min_val = sample_df[variable_column].min()
max_val = sample_df[variable_column].max()

cmap = cm.get_cmap('magma', 256)

def get_color(x, min_val, max_val, colormap):
    if pd.isna(x):
        return "#cccccc" 
    norm_val = (x - min_val) / (max_val - min_val)
    rgba_color_float = colormap(norm_val)

    rgba_color_int = [int(x * 255) for x in rgba_color_float]
    return rgba_color_int

df['color_rbga'] = df[variable_column].apply(lambda x: get_color(x, min_val, max_val, cmap))

layer = pdk.Layer(
    'GeoJsonLayer',
    data=sample_df,
    get_position=['lon', 'lat'],
    auto_highlight=True,
    get_radius=100000,
    get_fill_color='color_rgba', 
    pickable=True
)

view_state = pdk.ViewState(
    latitude=39.8283,
    longitude=-98.5795, zoom=3,
    pitch=0, bearing=0
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>County:</b> {County Name}<br/>Value: {variable_column}"
    }
)

st.pydeck_chart(deck)