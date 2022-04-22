from src.clients.base.baseClient import start_base_client
import dataReading


def main():
    start_base_client(dataReading.read_live_cam)


if __name__ == "__main__":
    main()
