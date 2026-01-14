import datetime
from app.models.telemetry import TelemetryPacket

def main() -> None:
    now = datetime.datetime.now(datetime.timezone.utc)
    packet = TelemetryPacket(
        timestamp=now,
        sol=912,
        battery_level=78.4,
        wheel_torque=[12.1, 11.9, 12.3, 12.0],
        temperature_internal=-12.4,
        temperature_external=-63.1,
        radiation_level=0.82,
        gps_lat=-4.5895,
        gps_lon=137.4417,
        error_flags=['OK'],
        note='Initial test packet'
    )
    print(packet)
    print()
    print(packet.model_dump_json(indent=2))


if __name__ == '__main__':
    main()
