from flask import Flask, render_template, request, jsonify
from influxdb import InfluxDBClient

app = Flask(__name__)

# Connect to InfluxDB on the storage node (adjust host/port as needed)
influx_client = InfluxDBClient(host='10.0.0.193', port=8086)
influx_client.switch_database('sensor_data')

# Home route that shows a welcome page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to ingest sensor data (e.g., from your ESP32)
@app.route('/ingest', methods=['POST'])
def ingest():
    data = request.get_json()
    print("Received data:", data)
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
        return jsonify({"message": "Data ingested successfully"}), 200
    except Exception as e:
        print("Error writing data:", e)
        return jsonify({"message": "Failed to ingest data", "error": str(e)}), 500

# Dashboard route that queries the database and displays sensor data
@app.route('/dashboard')
def dashboard():
    # Example query: get the latest 10 records from the 'environment' measurement.
    result = influx_client.query('SELECT * FROM environment ORDER BY time DESC LIMIT 10')
    data_points = list(result.get_points())
    return render_template('dashboard.html', data=data_points)

if __name__ == '__main__':
    # Run the Flask app. For production, consider using a WSGI server like Gunicorn.
    app.run(host='0.0.0.0', port=5000, debug=True)