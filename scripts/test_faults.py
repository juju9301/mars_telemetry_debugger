from app.generator.generator import generate_random_packet
from app.generator.fault_injector import FaultInjector

def main() -> None:
    packet = generate_random_packet()
    print(packet.model_dump_json(indent=2))

    fault_injector = FaultInjector(fault_probability=1.0)
    injected = fault_injector.maybe_inject_fault(packet)
    print(injected.model_dump_json(indent=2))


if __name__ == '__main__':
    main()