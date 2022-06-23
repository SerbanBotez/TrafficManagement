from influxdb_client.client import influxdb_client
from omegaconf import OmegaConf

config = OmegaConf.load('config.yaml')


def get_database_connection():
    token = config.DATABASE.TOKEN
    org = config.DATABASE.ORG
    url = config.DATABASE.URL

    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    return client
