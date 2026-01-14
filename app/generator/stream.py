import asyncio
from typing import AsyncGenerator

from app.generator.generator import generate_random_packet


async def telemetry_stream(sol: int = 0, interval: float = 1.0) -> AsyncGenerator:
    """
    Asyncronous generator that yields telemetry packets.
    sol: Starting Martian day.
    interval: Delay between packets in seconds.
    """

    current_sol = sol
    num_packets = 0

    while True:
        packet = generate_random_packet(sol=current_sol)
        yield packet

        # Increase sol every ~1000 packets
        num_packets += 1
        if num_packets > 5:
            current_sol += 1
            num_packets = 1

        await asyncio.sleep(interval)