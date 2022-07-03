from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS


def write_data(influx_client, client_type, car_count):
    bucket = "TrafficManagementBucket"

    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    point = Point(client_type).field("car_count_value", car_count)
    write_api.write(bucket=bucket, org="TrafficManagementOrganization", record=point)


def write_sensor_data(influx_client, sensor_data):
    bucket = "TrafficManagementBucket"
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    weather_point = Point("weather").field("weather_value", sensor_data['data']['weather'])
    temperature_point = Point("weather").field("temperature_tag_value", sensor_data['data']['temperature'])
    write_api.write(bucket=bucket, org="TrafficManagementOrganization", record=weather_point)
    write_api.write(bucket=bucket, org="TrafficManagementOrganization", record=temperature_point)
