import dataReading
from src.clients.base.baseClient import start_base_client


def main():
    start_base_client(dataReading.read_live_youtube_video)


if __name__ == "__main__":
    main()
