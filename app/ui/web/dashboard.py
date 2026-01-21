import json
import asyncio
import streamlit as st
import websockets
import pandas as pd

st.set_page_config(page_title="Mars Telemetry Dashboard", layout="wide")

st.title("🚀 Mars Telemetry Dashboard")

# Keep websocket connection alive across reruns
if "ws_charts" not in st.session_state:
    st.session_state.ws_charts = None

# History buffer for charts
if "history" not in st.session_state:
    st.session_state.history = []


async def connect_ws():
    if st.session_state.ws_charts is None:
        st.session_state.ws_charts = await websockets.connect("ws://localhost:8000/ws/telemetry")


async def stream_loop():
    await connect_ws()

    # Chart placeholders
    st.subheader('Live temporary charts')
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    battery_chart = col1.empty()
    temp_chart = col2.empty()
    torque_chart = col3.empty()
    torque_chart = col4.empty()
    radiation_chart = col4.empty()

    while True:
        try:
            message = await st.session_state.ws_charts.recv()
            data = json.loads(message)

            # Update packet info

            packet = data["packet"]

            # If packet is a JSON string, decode it
            if isinstance(packet, str):
                packet = json.loads(packet)

            # Add to history

            st.session_state.history.append({
                "battery": packet['battery_level'],
                "temp_internal": packet['temperature_internal'],
                "temp_external": packet['temperature_external'],
                "radiation": packet['radiation_level'],
                "wheel_0": packet['wheel_torque'][0],
                "wheel_1": packet['wheel_torque'][1],
                "wheel_2": packet['wheel_torque'][2],
                "wheel_3": packet['wheel_torque'][3],
                "sol": packet['sol'],
            })


            # Keep only last 200 packets

            st.session_state.history = st.session_state.history[-200:]

            # Convert to dataframe

            df = pd.DataFrame(st.session_state.history)

            # Update charts

            battery_chart.line_chart(data=df, x="sol", y="battery")
            temp_chart.line_chart(df[["temp_internal", "temp_external"]])
            torque_chart.line_chart(df[["wheel_0", "wheel_1", "wheel_2", "wheel_3"]])
            radiation_chart.line_chart(df["radiation"])

            await asyncio.sleep(0.5)

        except Exception as e:
            st.error(f"Connection lost: {e}")
            st.session_state.ws = None
            await asyncio.sleep(1)
            await connect_ws()


# Run the async loop inside Streamlit
asyncio.run(stream_loop())

# Prevent Streamlit from re-running the script
st.stop()