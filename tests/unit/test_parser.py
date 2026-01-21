import pytest
from app.parser import TelemetryParser

def test_parser_valid_packet():
    parser = TelemetryParser()
    packet = {
        "battery_level": 82,
        "temperature_internal": 12,
        "temperature_external": -55,
        "radiation_level": 0.12,
        "wheel_torque": [12.3, 10.2, 9.8, 11.1],
        "sol": 342,
        "gps_lat": -4.5895,
        "gps_lon": 137.4417,
    }
    result = parser.parse(packet)
    assert result.errors == []
    assert result.packet.battery_level == 82
