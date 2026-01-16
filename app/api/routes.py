import asyncio
from fastapi import APIRouter, WebSocket

from app.generator.stream import telemetry_stream
from app.generator.fault_injector import FaultInjector

router = APIRouter()

@router.websocket('/ws/telemetry')
async def telemetry_websocket(websocket: WebSocket):
    """
    WebSocket endpoint that streams processed telemetry packets.
    """
    await websocket.accept()

    injector = FaultInjector(fault_probability=0.3)

    async for result in telemetry_stream(
        sol=342,
        interval=1.0,
        injector=injector):

        # Convert ProcessedPacket into JSON-serializable dict

        payload = {
            "packet": result.packet.model_dump(mode="json"),
            "parser_errors": result.parser_errors,
            "anomalies": result.anomalies,
        }

        await websocket.send_json(payload)

        # If the client disconnects, break the loop

        # try:
        #     await websocket.receive_text()
        # except Exception:
        #     break

        await asyncio.sleep(0.01)