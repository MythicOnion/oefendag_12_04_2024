import folium
from folium import plugins
from folium.plugins import MarkerCluster, FastMarkerCluster
import pandas as pd

def render_map(location=[52.155499, 5.387740], zoom_start=7, map_width=1500, map_height=800, gdf=pd.DataFrame()):

    ## Create the basic map
    m = folium.Map(location=location, zoom_start=7, tiles = None)
    
    ## Add a basic OpenStreetMap (OSM) tile
    folium.TileLayer(tiles = 'openstreetmap', name = "OSM BASIC").add_to(m)
    
    ## Add an OSM-Dark tile
    folium.TileLayer(tiles = "https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png",  
                     name="OSM DARK", attr="OpenStreetMap Dark | <a href=https://wiki.openstreetmap.org/wiki/Tile_servers</a>").add_to(m)
    
    ## Add another tile, but this time with ESRI-satellite imagery
    folium.TileLayer(tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", name = "ESRI Worldview", 
                     attr="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community").add_to(m)

    marker_cluster = MarkerCluster(options={"disableClusteringAtZoom":"12", "zoomToBoundsOnClick":"true"}).add_to(m)
    for idx, row in gdf.iterrows():
        popup_text = f"<b>Station</b>: {row.description}<br><br><b>Aantal fietsen</b>: {row.n_ov_bikes}" 
        folium.Marker(location=[row.geometry.y, row.geometry.x], popup=popup_text).add_to(marker_cluster) 
    
    ## Adding a button to control which map tile layer to use
    folium.LayerControl().add_to(m)
    
    ## Adding a method to draw polygons on your map
    draw = plugins.Draw(export=True)
    draw.add_to(m)
    
    measurement_control = plugins.MeasureControl()
    measurement_control.add_to(m)  
    
    return m

def find_lat_lon_column_index(df):
    columns = df.columns
    lat = None
    lon = None
    i = -1
    for column in columns:
        i+=1
        column = column.lower()
        if not lat:
            if column == "lat" or column == "latitude" or column == "breedtegraad" or column == "lt" or column == "lat.":
                index_lat = i
        if not lon:
            if column == "lon" or column == "longitude" or column == "lengtegraad" or column == "lng" or column == "lon.":
                index_lon = i
    return index_lat, index_lon
