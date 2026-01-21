import json
import asyncio
import streamlit as st 
import websockets
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Mars Rover Map", layout="wide")

st.title("Mars Rover Position")

map_placeholder = st.empty()

if "ws_map" not in st.session_state:
    st.session_state.ws_map = None

if "history_map" not in st.session_state:
    st.session_state.history_map = []

async def connect_ws():
    if st.session_state.ws_map is None:
        st.session_state.ws_map = await websockets.connect("ws://localhost:8000/ws/telemetry")

async def stream_loop():
    await connect_ws()

    while True:
        try:
            message = await st.session_state.ws_map.recv()
            data = json.loads(message)

            packet = data['packet']
            if isinstance(packet, str):
                packet = json.loads(packet)

            st.session_state.history_map.append({
                "lat": packet['gps_lat'],
                "lon": packet['gps_lon'],
                "sol": packet['sol'],
            })

            st.session_state.history_map = st.session_state.history_map[-200:]

            df = pd.DataFrame(st.session_state.history_map)

             # Mars tile layer
            mars_tiles = (
                "https://planetarymaps.usgs.gov/mosaic/"
                "Mars_Viking_MDIM21_ClrMosaic_global_232m/tiles/{z}/{x}/{y}.png"
            )

            # Rover marker
            rover_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df.tail(1),
                get_position=["lon", "lat"],
                get_color=[255, 0, 0],
                get_radius=200,
            )

                      # Rover path
            path_layer = pdk.Layer(
                "PathLayer",
                data=[{"path": df[["lon", "lat"]].values.tolist()}],
                get_color=[255, 255, 0],
                width_scale=10,
                width_min_pixels=2,
            )

            view_state = pdk.ViewState(
                latitude=df["lat"].iloc[-1],
                longitude=df["lon"].iloc[-1],
                zoom=12,
                pitch=0,
            )

            tile_layer=pdk.Layer(
                "TileLayer",
                data=mars_tiles,
                min_zoom=0,
                max_zoom=18,
                tile_size=256,
            )

            mars_map = pdk.Deck(
                layers=[tile_layer, rover_layer, path_layer],
                initial_view_state=view_state,
                map_provider=None,
                map_style=None,
            )

            map_placeholder.pydeck_chart(mars_map)

            await asyncio.sleep(0.5)

        except Exception as e:
            st.error(f"Connection lost: {e}")
            st.session_state.ws = None
            await asyncio.sleep(1)
            await connect_ws()


asyncio.run(stream_loop())
st.stop()




