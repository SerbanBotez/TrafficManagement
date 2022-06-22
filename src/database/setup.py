from influxdb_client.client import influxdb_client


def get_database_connection():
    # TODO move this to a secret
    token = '8OQVJ79gKTjoLPuaQGItdz8XOb_MaRdLGErz5I6TK0wJI68sXXeIaaKYL3j0tdKxUupCaSKtlD5lzrnovu-HXw=='
    org = "TrafficManagementOrganization"
    url = "https://westeurope-1.azure.cloud2.influxdata.com"

    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    return client
