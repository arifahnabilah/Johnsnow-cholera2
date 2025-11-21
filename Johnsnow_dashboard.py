import streamlit as st
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(page_title="Cholera Death Map", layout="wide")
st.title("Cholera Death Dashboard (GeoJSON Version)")

# ------------------------------
# 1. LOAD GEOJSON DATA
# ------------------------------
with open('Cholera_Deaths.geojson', 'r') as f:
    deaths_geojson = json.load(f)
with open('Pumps.geojson', 'r') as f:
    pumps_geojson = json.load(f)

# Get center from deaths data
death_coords = [feat['geometry']['coordinates'] for feat in deaths_geojson['features']]
lats = [coord[1] for coord in death_coords]
lons = [coord[0] for coord in death_coords]
center = [sum(lats)/len(lats), sum(lons)/len(lons)]

# ------------------------------
# 2. CREATE FOLIUM MAP
# ------------------------------
m = folium.Map(location=center, zoom_start=16)

# Add deaths as red circle markers
for coord in death_coords:
    folium.CircleMarker(
        location=[coord[1], coord[0]],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.8
    ).add_to(m)

# Add pumps as blue markers
for feat in pumps_geojson['features']:
    pump_coord = feat['geometry']['coordinates']
    folium.Marker(
        location=[pump_coord[1], pump_coord[0]],
        popup="Water Pump",
        icon=folium.Icon(color="blue", icon="tint", prefix="fa")
    ).add_to(m)

# ------------------------------
# 3. DISPLAY IN STREAMLIT
# ------------------------------
st.subheader("Interactive Cholera Map")
st_folium(m, width=1000, height=600)