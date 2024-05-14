# streamlit run app.py --theme.primaryColor="#32cd32" --server.maxUploadSize 100000

import geopandas as gpd
import pandas as pd
import rasterio
import contextily as cx
import folium
from folium import plugins
import streamlit_folium as st_folium
import streamlit as st
from streamlit import session_state as sst
from folium.plugins import MarkerCluster, FastMarkerCluster
import requests

from utils import render_map, find_lat_lon_column_index

if 'refresh_map' not in sst:
    sst["refresh_map"] = False

if 'map' not in sst:
    sst["map"] = False

if "mapbutton" not in sst:
    sst["mapbutton"] = False

if "data_uploaded" not in sst:
    sst["data_uploaded"] = False

if "gdf" not in sst:
    sst["gdf"] = pd.DataFrame()
    
if "API_data_received" not in sst:
    sst["API_data_received"] = False

### Setting default lat/lon
base_lat = 52.155499
base_lon = 5.387740

map_width = 1500
map_height = 800


### Setting page configuration
st.set_page_config(page_title="Coole geo page", page_icon="🌐", layout="wide", initial_sidebar_state="expanded", menu_items=None)

st.title("🌐Basis geo-applicatie🛰️", anchor=None)
st.header("Eerste opzet")
st.sidebar.title("Menu")

MapTab, DataTab = st.tabs(["Map", "Data"])

datafile = st.sidebar.file_uploader(label="Heb je vectordata in een .csv-file? Upload die hier!", type="csv")
if datafile:
    if datafile.name.endswith("csv"):
        data = pd.read_csv(datafile)
        
        index_lat, index_lon = find_lat_lon_column_index(data)
        
        lat_col, lon_col = st.sidebar.columns(2)
        with lat_col:
            lat = st.sidebar.selectbox("Selecteer hier je kolom met **breedtegraad** erin", data.columns, index=index_lat)
        with lon_col:
            lon = st.sidebar.selectbox("Selecteer hier je kolom met **lengtegraad** erin", data.columns, index=index_lon)
            
        selected_epsg = st.sidebar.selectbox("Welke EPSG gebruik je voor je data?", [4326, 3857, "Anders..."])
        if selected_epsg == "Anders...":
            selected_epsg =  st.sidebar.number_input("Type hier je EPSG in.", value=4326)

        data_uploaded = st.sidebar.button(label="Visualiseer mijn data!", type="primary")   
        if data_uploaded == True:
            sst["data_uploaded"] = True
            geometry = gpd.points_from_xy(data[lon], data[lat], crs=int(selected_epsg))
            gdf = gpd.GeoDataFrame(data, geometry=geometry)
            if selected_epsg != 4326:
                gdf = gdf.to_crs(4326)
            sst["gdf"] = gdf
    else:
        st.error("🔥Upload eens gewoon een .csv joh...!")  

api_data = st.sidebar.text_input(label="Heb je vectordata die je met een **API-call** wilt visualiseren? Voer de http(s)-link dan hier in! \n\n**Let op**: Alleen data in .csv-formaat werkt momenteel.")
if api_data and sst["API_data_received"] == False:
    try:
        data = requests.get(api_data)
        sst["API_data_received"] = True
    except:
        st.error("🔥Ongeldige API")
    if sst["API_data_received"] == True and sst["data_uploaded"] == False:
        # df = pd.DataFrame(data.json())
        # df = df.transpose()
    
        ## Silly stuff  - remove later and replace with more generic script
        gdf = gpd.GeoDataFrame(data.json()["locaties"])
        gdf = gdf.transpose()
        n_ov_bikes_list = []
        for idx, row in gdf.iterrows():
            if "rentalBikes" in row["extra"].keys():
                n_ov_bikes = row["extra"]["rentalBikes"]
                n_ov_bikes_list.append(n_ov_bikes)
            else:
                n_ov_bikes_list.append(0)
        
        gdf["n_ov_bikes"] = n_ov_bikes_list
        gdf.reset_index(inplace=True)
        index_lat, index_lon = find_lat_lon_column_index(gdf)
        geometry = gpd.points_from_xy(gdf.iloc[:,index_lon], gdf.iloc[:, index_lat], crs="EPSG:4326")
        gdf = gpd.GeoDataFrame(gdf, geometry=geometry)
        sst["gdf"] = gdf   
        sst["data_uploaded"] = True
#     selected_epsg = st.sidebar.selectbox("Welke EPSG gebruik je voor je data?", [4326, 3857, "Anders..."])
#     if selected_epsg == "Anders...":
#         selected_epsg =  st.sidebar.number_input("Type hier je EPSG in.", value=4326)

#     data_uploaded = st.sidebar.button(label="Visualiseer mijn data!", type="primary")   
#     if data_uploaded == True:
#         sst["data_uploaded"] = True
#         geometry = gpd.points_from_xy(data[lon], data[lat], crs=int(selected_epsg))
#         gdf = gpd.GeoDataFrame(data, geometry=geometry)
#         if selected_epsg != 4326:
#             gdf = gdf.to_crs(4326)
#         sst["gdf"] = gdf    
        
with MapTab:
    ### Setting parameters for the height and width of the maps to be displayed
    # if not sst["map"]:
    if not sst["data_uploaded"]:
        sst["map"] = render_map(location=[52.155499, 5.387740], zoom_start=7, map_width=map_width, map_height=map_height)        
        map_folium = st_folium.st_folium(sst["map"], width = map_width, height = map_height)
    else:
        sst["map"] = render_map(location=[52.155499, 5.387740], zoom_start=7, map_width=map_width, map_height=map_height, gdf=sst["gdf"])    
        folium_map = st_folium.st_folium(sst["map"], width = map_width, height = map_height)

with DataTab:
    if datafile or sst["API_data_received"]:
        st.markdown("Eerste 100 regels van je data")
        st.dataframe(sst["gdf"].loc[:, sst["gdf"].columns != "geometry"].head(100))

        




