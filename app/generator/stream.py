import asyncio
from typing import AsyncGenerator, Optional

from app.generator.generator import generate_random_packet
from app.generator.fault_injector import FaultInjector


async def telemetry_stream(
        sol: int = 0, 
        interval: float = 1.0,
        injector: Optional[FaultInjector] = None) -> AsyncGenerator:
    """
    Asyncronous generator that yields telemetry packets.
    sol: Starting Martian day.
    interval: Delay between packets in seconds.
    optionally applies fault injection.
    """

    current_sol = sol
    num_packets = 0

    while True:
        packet = generate_random_packet(sol=current_sol)

        if injector is not None:
            packet = injector.maybe_inject_fault(packet)
            
        yield packet

        # Increase sol every ~1000 packets
        num_packets += 1
        if num_packets > 5:
            current_sol += 1
            num_packets = 1

        await asyncio.sleep(interval)