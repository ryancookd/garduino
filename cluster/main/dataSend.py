from flask import Flask, request, jsonify
from influxdb import InfluxDBClient

app = Flask(__name__)

# Connect to InfluxDB on the storage node (update host if needed)
influx_client = InfluxDBClient(host='10.0.0.193', port=8086)
influx_client.switch_database('sensor_data')

@app.route('/soil-data', methods=['POST'])
def ingest_data():
    data = request.get_json()
    print("Received data from ESP32:", data)

    try:
        json_body = [
            {
                "measurement": "environment",
                "fields": {
                    "soil_moisture": int(data.get("soil_moisture", 0)),
                    "temperature": float(data.get("temperature", 0.0))
                }
            }
        ]
        influx_client.write_points(json_body)
        return jsonify({"message": "Data written to InfluxDB successfully"}), 200
    except Exception as e:
        print("Error writing data to InfluxDB:", e)
        return jsonify({"message": "Failed to write data to InfluxDB"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
