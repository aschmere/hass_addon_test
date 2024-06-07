from flask import Flask, request, jsonify, send_file
import json
import io
import pickle
import xarray as xr
import main
import logging

app = Flask(__name__)

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

if __name__ == '__main__':
    app.logger.debug("Starting Flask app")
    app.run(host='0.0.0.0', port=5001)
