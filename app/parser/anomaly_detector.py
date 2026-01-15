from typing import List
from app.models.telemetry import TelemetryPacket


class AnomalyDetector:

    def detect(self, packet: TelemetryPacket) -> List[str]:
        anomalies: List[str] = []

        # Battery anomalies

        if packet.battery_level < 20:
            anomalies.append("Battery critically low")
        if packet.battery_level > 100:
            anomalies.append('Battery reading out of range (>100%)')

        #Temperature anomalies
        if packet.temperature_internal is None:
            anomalies.append('Missing temperature_internal value')
        if packet.temperature_internal < -50 or packet.temperature_internal > 50:
            anomalies.append(f'Internal temperature out of expected range, {packet.temperature_internal}')

        if packet.temperature_external < -150 or packet.temperature_external > 20:
            anomalies.append(f'External temperature out of expected range, {packet.temperature_external}')

        # Radiation anomalies

        if packet.radiation_level > 5.0:
            anomalies.append('Radiation spike detected.')

        # Wheel torque anomalies
        for i,torque in enumerate(packet.wheel_torque):
            if torque > 20.0:
                anomalies.append(f'Wheel {i} torque spiked at {torque} (possible jam).')

        return anomalies
    