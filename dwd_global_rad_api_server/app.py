from flask import Flask, request, jsonify, send_file
import json
import io
import pickle
import xarray as xr
import main
import logging
import dwd_global_radiation as dgr

app = Flask(__name__)

# Instantiate main object
objGlobalRadiation = dgr.GlobalRadiation()
# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/process', methods=['POST'])
def process():
    if 'dataset' not in request.files or 'locations' not in request.form:
        app.logger.error("Missing dataset or locations parameter")
        return jsonify({'error': 'Missing dataset or locations parameter'}), 400

    dataset_file = request.files['dataset']
    locations = json.loads(request.form['locations'])

    try:
        app.logger.info(f"Locations received: {locations}")

        app.logger.info("Loading dataset")
        ds = pickle.load(dataset_file)
        app.logger.info("Dataset loaded successfully")

        app.logger.info("Creating animation")
        output_file = main.create_animation(ds, locations)
        app.logger.info("Animation created successfully")

        return send_file(output_file, as_attachment=True, download_name='forecast_animation.gif', mimetype='image/gif')
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500
# Instantiate main object
objGlobalRadiation = dgr.GlobalRadiation()

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = objGlobalRadiation.locations
    if not locations:
        return jsonify({'error': 'No locations found'}), 404
    
    serializable_locations = [loc.to_dict() for loc in locations]
    print(json.dumps(serializable_locations, indent=2))  # Pretty-print the JSON data
    return jsonify(serializable_locations)

@app.route('/locations', methods=['POST'])
def add_location():
    data = request.json
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    try:
        # Call the add_location method from the GlobalRadiation class
        objGlobalRadiation.add_location(name=name, latitude=latitude, longitude=longitude)
        return jsonify({'status': 'Location added successfully'}), 200
    except ValueError as e:
        # Handle the exception and return a 400 Bad Request response
        return jsonify({'error': str(e)}), 400

@app.route('/locations/<name>', methods=['GET'])
def get_location_by_name(name):
    """Fetch a specific location by name."""
    location = objGlobalRadiation.get_location_by_name(name)
    if location is None:
        return jsonify({'error': 'Location not found'}), 404
    
    return jsonify(location.to_dict())

@app.route('/forecasts', methods=['GET'])
def fetch_forecasts():
    """Check if forecast data is available."""
    # Fetch the forecast data from the DWD servers
    objGlobalRadiation.fetch_forecasts()

    forecast_data = objGlobalRadiation.forecast_data
    if forecast_data is None:
        return jsonify({'error': 'Forecast data not found'}), 404

    return jsonify({'message': 'Forecast data is available'}), 200

@app.route('/measurements', methods=['GET'])
def fetch_measurements():
    """Fetch the measurement data for a specific location by name."""
    
    # Get the 'hours' query parameter from the request, default to 3 if not provided
    hours = request.args.get('hours', default=3, type=int)
    # Fetch the measurement data from the DWD servers
    objGlobalRadiation.fetch_measurements(max_hour_age_of_measurement=hours)

    measurement_data = objGlobalRadiation.measurement_data
    if measurement_data is None:
        return jsonify({'error': 'Forecast data not found'}), 404

    return jsonify({'message': 'Measurement data is available'}), 200

@app.route('/locations/<name>', methods=['DELETE'])
def remove_location(name):
    """Remove a specific location by name."""
    try:
        objGlobalRadiation.remove_location(name)
        return jsonify({'status': 'Location removed successfully'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
@app.route('/status', methods=['GET'])

def get_status():
    """Endpoint to check if the API server is running."""
    return '', 204  # No Content status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
