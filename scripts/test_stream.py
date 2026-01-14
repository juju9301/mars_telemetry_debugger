import asyncio
from app.generator.stream import telemetry_stream

async def main() -> None:
    async for packet in telemetry_stream(sol=912, interval=1.0):
        print(packet.model_dump_json(indent=2))
        print('-' * 40)


if __name__ == "__main__":
    asyncio.run(main())