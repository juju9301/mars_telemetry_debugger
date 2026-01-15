import asyncio

from app.generator.stream import telemetry_stream
from app.generator.fault_injector import FaultInjector


async def main() -> None:
    injector = FaultInjector(fault_probability=0.5)

    async for result in telemetry_stream(
        sol=305,
        interval=1.0,
        injector=injector):

        print(result.packet.model_dump_json())
        print(result.parser_errors)
        print(result.anomalies)

        print('-' * 50)




if __name__ == '__main__':
    asyncio.run(main())