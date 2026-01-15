import asyncio

from app.generator.stream import telemetry_stream
from app.generator.fault_injector import FaultInjector


async def main() -> None:
    injector = FaultInjector(fault_probability=0.5)

    async for packet in telemetry_stream(
        sol=834,
        interval=1.0,
        injector=injector):
        print(packet.model_dump_json())
        print('-' * 40)


if __name__ == '__main__':
    asyncio.run(main())
        
