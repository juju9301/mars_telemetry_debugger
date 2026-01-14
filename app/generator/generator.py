import random
from datetime import datetime, timezone
from typing import List

from app.models.telemetry import TelemetryPacket


def generate_random_torque(num_wheels: int = 4) -> List[float]:
    """Generate random torque values for wheels. 
    Typical value range is around 10-15 Nm."""
    return [round(random.uniform(10.0, 15.0), 2) for _ in range(num_wheels)]

def generate_random_packet(sol: int = 0) -> TelemetryPacket:
    """
    Create a single packet with random realistic values.
    """
    packet = TelemetryPacket(
        timestamp=datetime.now(timezone.utc),
        sol=sol,
        battery_level=round(random.uniform(40.0, 100.0), 2),
        wheel_torque=generate_random_torque(),
        temperature_internal=round(random.uniform(-20.0, 0.0), 2),
        temperature_external=round(random.uniform(-90.0, -40.0), 2),
        radiation_level=round(random.uniform(0.1, 1.5), 2),
        gps_lat=round(random.uniform(-10.0, 10.0), 4),
        gps_lon=round(random.uniform(130.0, 150.0), 4),
        error_flags=['OK'],
        note=None,
    )

    return packet

