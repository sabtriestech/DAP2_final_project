import streamlit as st
import pandas as pd
import geopandas as gpd
from os.path import join
import os
import numpy as np
import matplotlib.cm as cm
import pydeck as pdk
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import requests
import altair as alt

import warnings
warnings.filterwarnings('ignore')
alt.renderers.enable("png")
alt.data_transformers.disable_max_rows()

BASE_DIR = Path(__file__).parent.parent

st.set_page_config(page_title='Economic Mobility', layout="wide")
st.title('Economic Mobility, Wages, Housing, and Crime')

def intro():
    import streamlit as st
    st.markdown('This dashboard allows you to explore economic mobility data and its ties to other socioeconomic indicators. To begin, select an indicator of choice')
intro()

variable_choice = st.selectbox(
    "Select a Variable",
    options= ["Violent Crime", "Property Crime", "HHI",
               "Housing Prices for Low Earners", "Housing Prices for High Earners"]
)

#load and clean data
@st.cache_data
def load_data():
    df = gpd.read_file("C:/Users/s_bea/DAP2_final_project/data/derived_data/Dashboard Data with Geography.shp")
    pctile95v = df['Violent cr'].quantile(0.95)
    df["Violent crime_rate_winsor"] = np.where(df["Violent cr"] > pctile95v, 
                                                     pctile95v, 
                                                     df["Violent cr"]) 
    pctile95p = df['Property c'].quantile(0.95)
    df["Property crime_rate_winsor"] = np.where(df["Property c"] > pctile95p, 
                                                     pctile95p, 
                                                     df["Property c"]) 
    df["HHI_winsor"] = np.where(df['Inverse HH'] < 1, 1, df["Inverse HH"])
    pctile95hhi = df['Inverse HH'].quantile(0.95)
    df["HHI_winsor"] = np.where(df["HHI_winsor"] > pctile95hhi, pctile95hhi, df["HHI_winsor"]) 

    return df

df = load_data()

#dictionary for selected columns:
selected_column = {'Housing Prices for Low Earners':'Median Hou',
                   'Housing Prices for High Earners': 'Median H_1',
                    'Property Crime': 'Property crime_rate_winsor',
                    'Violent Crime':'Violent crime_rate_winsor',
                    'HHI': 'HHI_winsor'}

variable_column = selected_column[variable_choice]

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"Mapping Data on {variable_choice}")
    min_val = df[variable_column].min()
    max_val = df[variable_column].max()

    cmap = cm.get_cmap('magma', 256)

    def get_color(x, min_val, max_val, colormap):
        if pd.isna(x):
            return "#cccccc" 
        norm_val = (x - min_val) / (max_val - min_val)
        rgba_color_float = colormap(norm_val)

        rgba_color_int = [int(x * 255) for x in rgba_color_float]
        return rgba_color_int

    df['color_rgba'] = df[variable_column].apply(lambda x: get_color(x, min_val, max_val, cmap))

    layer = pdk.Layer(
        'GeoJsonLayer',
        data=df,
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
            "html": "<b>County:</b> {County Name}<br/>Value:  {" + variable_column + "}"
        }
    )

    st.pydeck_chart(deck)
with col2:
    st.subheader(f"Histogram of Values for {variable_choice}")
    st.markdown("#### Filters")
    # Type of County
    all = st.checkbox("All", value=True)
    under_50 = st.checkbox("Show only >50% Mobility for 25th Percentile", value=False)
    over_50 = st.checkbox("Show Only <50% Mobility for 25th Percentile", value=False)
    filtered_df = df.copy()

    if under_50:
        filtered_df = filtered_df[filtered_df['kr26_p25_coef'] <= 0]
    elif over_50:
        filtered_df = filtered_df[filtered_df['kr26_p25_coef'] >= 0]

    sample_df = filtered_df

    chart_data = sample_df[[variable_column]]
    chart = alt.Chart(chart_data).mark_bar().encode(
        alt.X(f"{variable_column}:Q", bin=True, title=f'{variable_choice}'),
        alt.Y('count()', title = 'Frequency'),
        color=alt.value('#FEA96C')).properties(
        title=f'Distribution of Counties on Variable')

    mean_line = alt.Chart(chart_data).mark_rule(color='#A52C7A',size=4).encode(
    x=alt.X(f'mean({variable_column}):Q'))

    label = alt.Chart(chart_data).mark_text(
    align='left',
    baseline='middle',
    dx=5,
    size=10,
    color='#000004').encode(
    x=alt.X(f'mean({variable_column}):Q'),
    y=alt.value(10),
    text=alt.Text(f'mean({variable_column}):Q', format='.2f'))
  
    plot = chart + mean_line + label
    plot

