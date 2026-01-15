from typing import List
from app.models.telemetry import TelemetryPacket


class ProcessedPacket:
    """
    Represents the full result of processing a telemetry packet:
    - validated packet
    - parser errors
    - anomaly warnings
    """

    def __init__(
            self,
            packet: TelemetryPacket,
            parser_errors: List[str],
            anomalies: List[str]):
        self.packet = packet
        self.parser_errors = parser_errors
        self.anomalies = anomalies