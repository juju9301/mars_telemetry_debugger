import asyncio
from typing import AsyncGenerator, Optional

from app.generator.generator import generate_random_packet
from app.generator.fault_injector import FaultInjector
from app.parser.parser import TelemetryParser
from app.parser.anomaly_detector import AnomalyDetector
from app.parser.result import ProcessedPacket


async def telemetry_stream(
        sol: int = 0, 
        interval: float = 1.0,
        injector: Optional[FaultInjector] = None) -> AsyncGenerator[ProcessedPacket, None]:
    """
    Asyncronous generator that yields telemetry packets.
    sol: Starting Martian day.
    interval: Delay between packets in seconds.
    optionally applies fault injection.

    Yields fully processed telemetry packet:
    - raw packet
    - parser validation errors
    - anomaly warnings
    """

    parser = TelemetryParser()
    detector = AnomalyDetector()

    current_sol = sol
    num_packets = 0

    while True:

        # Generate packet

        packet = generate_random_packet(sol=current_sol)

        # Apply faults

        if injector is not None:
            packet = injector.maybe_inject_fault(packet)
        
        # Parse and validate packet. Detect anomalies

        parsed = parser.parse(packet)
        anomalies = detector.detect(parsed.packet)

        yield ProcessedPacket(
            packet=parsed.packet,
            parser_errors=parsed.errors,
            anomalies = anomalies
        )

        # Increase sol every ~1000 packets. For testing purposes currently 5.
        num_packets += 1
        if num_packets > 5:
            current_sol += 1
            num_packets = 1

        await asyncio.sleep(interval)