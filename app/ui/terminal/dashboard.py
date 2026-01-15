from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import VerticalScroll

import asyncio

from app.generator.stream import telemetry_stream
from app.generator.fault_injector import FaultInjector


class TelemetryView(Static):
    """Widget that displays the latest telemetry packet"""

    def __init__(self):
        super().__init__(markup=False)

    def update_packet(self, packet, parser_errors, anomalies):
        text = "Telemetry Packet\n\n" + f"{packet}\n\n" + f"Parser Errors: {parser_errors}\n" + f"Anomalies: {anomalies}\n"
        self.update(text)

class TelemetryDashboard(App):
    CSS_PATH = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(TelemetryView())
        yield Footer()

    async def on_mount(self) -> None:
        """Start the telemetry stream when UI loads"""
        view = self.query_one(TelemetryView) 

        injector = FaultInjector(fault_probability=0.3)

        async def stream_loop():
            async for result in telemetry_stream(
                sol=678,
                interval=1.0,
                injector=injector):

                packet_json = result.packet.model_dump_json(indent=2)

                view.update_packet(
                    packet_json,
                    result.parser_errors,
                    result.anomalies
                )
        asyncio.create_task(stream_loop())   

def run_dashboard():
    TelemetryDashboard().run()