from src.clients.base.baseClient import start_base_client
import dataReading


def main():
    start_base_client(dataReading.read_local_video)


if __name__ == "__main__":
    main()
