from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route('/sensor', methods=['POST'])
def sensor_data():
    data = request.json
    light_value = data.get('light_value', None)
    
    if light_value is not None:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("sensor_data.txt", "a") as f:
            f.write(f"{timestamp}, {light_value}\n")
        print(f"Received light value: {light_value}")
        return jsonify({"message": "Data received"}), 200
    
    return jsonify({"message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
