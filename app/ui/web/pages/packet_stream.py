import json
import asyncio
import streamlit as st
import websockets
import pandas as pd

st.set_page_config(page_title="Mars Telemetry Dashboard", layout="wide")

st.title("🚀 Mars Telemetry Dashboard")

packet_box = st.empty()
errors_box = st.empty()
anomalies_box = st.empty()

# Keep websocket connection alive across reruns
if "ws" not in st.session_state:
    st.session_state.ws = None

async def connect_ws():
    if st.session_state.ws is None:
        st.session_state.ws = await websockets.connect("ws://localhost:8000/ws/telemetry")


async def stream_loop():
    await connect_ws()

    while True:
        try:
            message = await st.session_state.ws.recv()
            data = json.loads(message)

            packet = data['packet']

            # If packet is a JSON string, decode it
            if isinstance(packet, str):
                packet = json.loads(packet)

            packet_box.json(packet)
            errors_box.error(data["parser_errors"] or "No parser errors")
            anomalies_box.warning(data["anomalies"] or "No anomalies")

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