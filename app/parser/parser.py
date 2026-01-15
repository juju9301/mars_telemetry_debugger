from typing import Tuple, List
from pydantic import ValidationError

from app.models.telemetry import TelemetryPacket


class ParsedPacket:
    """
    Result of parsing a telemetry packet.
    Contains the validated packet and parser-level errors.
    """

    def __init__(self, packet: TelemetryPacket, errors: List[str]):
        self.packet = packet
        self.errors = errors

class TelemetryParser:
    """
    Validates telemetry packets using pydantic.
    """

    def parse(self, packet: TelemetryPacket) -> ParsedPacket:
        """
        Validate the packet and collect any structural errors.
        """
        errors: List[str] = []
        try:
            validated = TelemetryPacket(**packet.model_dump())
        except ValidationError as e:
            errors.append(f'Validation error: {e}')
            return ParsedPacket(packet, errors)
        
        #Other dummy structural checks, to be expanded later
        if validated.temperature_external is None:
            errors.append("Missing field: temperature_external")

        if validated.battery_level is None:
            errors.append("Missing field: battery_level")
        
        return ParsedPacket(validated, errors)



