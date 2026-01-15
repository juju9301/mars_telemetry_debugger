from app.generator.generator import generate_random_packet
from app.generator.fault_injector import FaultInjector
from app.parser.parser import TelemetryParser
from app.parser.anomaly_detector import AnomalyDetector


def main() -> None:
    injector = FaultInjector(fault_probability=1.0)
    parser = TelemetryParser()
    detector = AnomalyDetector()

    packet = generate_random_packet(sol=67)
    faulty = injector.maybe_inject_fault(packet)

    parsed = parser.parse(faulty)
    anomalies = detector.detect(parsed.packet)

    print(parsed.packet.model_dump_json())
    print('-' *30)
    print(parsed.errors)
    print('-' *30)
    print(anomalies)

if __name__ == "__main__":
    main()