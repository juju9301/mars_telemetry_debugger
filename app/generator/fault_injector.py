import random
from typing import Callable
from app.models.telemetry import TelemetryPacket


class FaultInjector:
    """
    Applies random or specific faults to telemetry packets
    """

    def __init__(self, fault_probability: float = 0.1):
        """
        Args:
            fault_probability: chance 1/10 that a packet will be modified.
        """
        self.fault_probability = fault_probability

    def maybe_inject_fault(self, packet: TelemetryPacket) -> TelemetryPacket:
        """
        Randomly decides whether to inject fault into the packet
        """
        if random.random() > self.fault_probability:
            return packet
        
        fault = random.choice([
            self._corrupt_battery,
            self._missing_field,
            self._out_of_range_temperature,
            self._sensor_drift,
            self._wheel_jam
        ])

        return fault(packet)
    
    def _corrupt_battery(self, packet: TelemetryPacket) -> TelemetryPacket:
        """
        Sets battery charge level to a nonsense value.
        """
        packet.battery_level = random.choice([-10, 105, 102])
        packet.error_flags = ['WARN']
        packet.note = 'Battery corruption fault'
        return packet
    
    def _missing_field(self, packet: TelemetryPacket) -> TelemetryPacket:
        """Removes a value from field. For now only for temperature_external"""
        packet.temperature_external = None
        packet.error_flags = ['ERROR']
        packet.note = 'Missing field fault'
        return packet
    
    def _out_of_range_temperature(sef, packet: TelemetryPacket) -> TelemetryPacket:
        """Creates extreme temperature values"""
        packet.temperature_internal = random.choice([-200, 200])
        packet.error_flags = ['WARN']
        packet.note = 'Out-of-range temperature'
        return packet
    
    def _sensor_drift(self, packet: TelemetryPacket) -> TelemetryPacket:
        """Sets out of range radiation level"""
        drift = random.uniform(-5.0, 5.0)
        packet.radiation_level += drift
        packet.error_flags = ['WARN']
        packet.note = f'Sensor drift: {drift:+.2f}'
        return packet
    
    def _wheel_jam(self, packet: TelemetryPacket) -> TelemetryPacket:
        """Simulates a wheel jam by spiking torque on one of the wheels."""
        jammed_index = random.randint(0, len(packet.wheel_torque) -1)
        packet.wheel_torque[jammed_index] = random.uniform(20.0, 50.0)
        packet.error_flags = ['ERROR']
        packet.note = f'Wheel jam on wheel {jammed_index}'
        return packet
        
    