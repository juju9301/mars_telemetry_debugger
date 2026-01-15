from typing import List
from app.models.telemetry import TelemetryPacket

def is_out_of_range(value, low, high):
    if value is None:
        return False
    if not isinstance(value, (int, float)):
        return False
    return value < low or value > high 


class AnomalyDetector:

    def detect(self, packet: TelemetryPacket) -> List[str]:
        anomalies: List[str] = []

        # Battery anomalies

        if is_out_of_range(packet.battery_level, 20, 100):
            anomalies.append('Battery reading out of range')

        #Temperature anomalies
        
        if is_out_of_range(packet.temperature_internal, -50, 50):
            anomalies.append(f'Internal temperature out of expected range, {packet.temperature_internal}')

        if is_out_of_range(packet.temperature_external, -150, 20):
            anomalies.append(f'External temperature out of expected range, {packet.temperature_external}')

        # Radiation anomalies

        if packet.radiation_level > 5.0:
            anomalies.append('Radiation spike detected.')

        # Wheel torque anomalies
        for i,torque in enumerate(packet.wheel_torque):
            if torque > 20.0:
                anomalies.append(f'Wheel {i} torque spiked at {torque} (possible jam).')

        return anomalies
    