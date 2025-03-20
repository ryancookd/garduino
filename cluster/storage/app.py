from influxdb import InfluxDBClient
import json

# Connect to InfluxDB
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('sensor_data')

# Read the data file (adjust path as needed)
with open('/mnt/storage/data.txt', 'r') as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            # Construct a JSON body for InfluxDB
            json_body = [
                {
                    "measurement": "soil_moisture",
                    "fields": {
                        "value": data.get("soil_moisture", 0)
                    }
                }
            ]
            client.write_points(json_body)
        except Exception as e:
            print(f"Error processing line: {e}")