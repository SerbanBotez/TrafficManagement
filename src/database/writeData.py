from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS


def write_data(influx_client, car_count):
    bucket = "TrafficManagementBucket"

    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    point = Point("vehicle_count").tag("car_count_tag_name", "car_count_tag_value").field("car_count_value", car_count)
    write_api.write(bucket=bucket, org="TrafficManagementOrganization", record=point)
