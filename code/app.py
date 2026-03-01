import streamlit as st
import pandas as pd
import altair as alt
import geopandas as gpd
from os.path import join
import numpy as np
import time
import re
import matplotlib.cm as cm
import pydeck as pdk

import warnings
warnings.filterwarnings('ignore')
alt.renderers.enable("png")
alt.data_transformers.disable_max_rows()

data_path = 'data/external'

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