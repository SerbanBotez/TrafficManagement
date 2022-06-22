import influxdb_client
import os
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#1
# TODO move this to a secret
token = '8OQVJ79gKTjoLPuaQGItdz8XOb_MaRdLGErz5I6TK0wJI68sXXeIaaKYL3j0tdKxUupCaSKtlD5lzrnovu-HXw=='
org = "TrafficManagementOrganization"
url = "https://westeurope-1.azure.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

#2
bucket = "TrafficManagementBucket"

write_api = client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
    point = (
        Point("vehicle_count")
            .tag("car_count_tag_name", "car_count_tag_value")
            .field("car_count_value", value)
    )
    write_api.write(bucket=bucket, org="TrafficManagementOrganization", record=point)
    time.sleep(1)  # separate points by 1 second

#3
query_api = client.query_api()

query = """from(bucket: "TrafficManagementBucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "vehicle_count")"""
tables = query_api.query(query, org="TrafficManagementOrganization")

for table in tables:
  for record in table.records:
    print(record)

#4
query_api = client.query_api()

query = """from(bucket: "TrafficManagementBucket")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="TrafficManagementOrganization")

for table in tables:
    for record in table.records:
        print(record)