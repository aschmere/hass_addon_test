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
# Configure logging with a custom formatter
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

# Remove the default Flask handlers if any
for handler in app.logger.handlers[:]:
    app.logger.removeHandler(handler)
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

app.logger.propagate = False


@app.route('/process', methods=['POST'])
def process():
    try:
        if 'dataset' in request.files:
            app.logger.info("Dataset provided in request")
            dataset_file = request.files['dataset']
            ds = pickle.load(dataset_file)
        else:
            app.logger.info("No dataset provided, fetching internally")
            objGlobalRadiation.fetch_forecasts()
            ds = objGlobalRadiation.forecast_data.all_grid_forecasts

        if 'locations' in request.form:
            app.logger.info("Locations provided in request")
            locations = json.loads(request.form['locations'])
        else:
            app.logger.info("No locations provided, using internal locations")
            locations = [{"lat": loc.latitude, "lon": loc.longitude} for loc in objGlobalRadiation.locations]

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
