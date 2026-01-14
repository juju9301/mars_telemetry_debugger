from app.generator.generator import generate_random_packet

def main() -> None:
    packet = generate_random_packet(sol=913)
    print(packet.model_dump_json(indent=2))


if __name__ == "__main__":
    main()