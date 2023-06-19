from flask import Flask, render_template, request, send_file, jsonify, current_app, url_for
import os
import json
from map_generator import main as generate_map
import cartopy.crs as ccrs
import logging
from datetime import datetime
import requests

logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)

def convert_coord(coord_str):
    if coord_str[-1].upper() in ('N', 'S', 'E', 'W'):
        direction = coord_str[-1].upper()
        coord = float(coord_str[:-1])
        if direction in ('S', 'W'):
            coord *= -1
    else:
        coord = float(coord_str)
    return coord

@app.route('/', methods=['GET', 'POST'])
def index():
    with open(os.path.join(app.root_path, 'static', 'locations.json'), 'r') as file:
        location_data = json.load(file)

    if request.method == 'POST':
        # Your existing POST handling code here
        pass
    else:
        location1_str = [location_data[0]['location1']['name'], location_data[0]['location1']['latitude'], location_data[0]['location1']['longitude']]
        location2_str = [location_data[0]['location2']['name'], location_data[0]['location2']['latitude'], location_data[0]['location2']['longitude']]
        location3_str = [location_data[1]['location1']['name'], location_data[1]['location1']['latitude'], location_data[1]['location1']['longitude']]
        location4_str = [location_data[1]['location2']['name'], location_data[1]['location2']['latitude'], location_data[1]['location2']['longitude']]

        plot_second_pair = True

        # Fetch location pairs
        location_pairs_response = requests.get(url_for('fetch_location_pairs'))
        #location_pairs_response = requests.get(flask.url_for('fetch_location_pairs'))
        #location_pairs_response = requests.get(url_for('fetch_location_pairs', _external=True))


        if location_pairs_response.status_code == 200:
            location_pairs = location_pairs_response.json()["location_pairs"]
        else:
            location_pairs = []

        return render_template('index.html',
                               filename_plate_carree=None,
                               filename_azimuthal_equidistant=None,
                               location1=location1_str,
                               location2=location2_str,
                               location3=location3_str if plot_second_pair else ["", "", ""],
                               location4=location4_str if plot_second_pair else ["", "", ""],
                               plot_second_pair=plot_second_pair,
                               location_data=location_data,
                               location_pairs=location_pairs)
        
@app.route('/get_location_pairs', methods=['GET'])
def fetch_location_pairs():
    with open(os.path.join(app.root_path, 'static', 'locations.json'), 'r') as file:
        location_data = json.load(file)

    pairs = []
    for i, pair in enumerate(location_data):
        pairs.append({
            "pairID": i,
            "pairName": f"{pair['location1']['name']} - {pair['location2']['name']}"
        })

    return jsonify({"location_pairs": pairs})

@app.route('/generate_map', methods=['POST'])
def generate_map_ajax():
    filename_plate_carree = None
    filename_azimuthal_equidistant = None

    location1_str = [request.form.get('location1Name'), request.form.get('location1Lat'), request.form.get('location1Lon')]
    location2_str = [request.form.get('location2Name'), request.form.get('location2Lat'), request.form.get('location2Lon')]

    plot_second_pair = 'plotSecondPair' in request.form

    location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
    location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]

    if None in location1 or None in location2 or "" in location1_str or "" in location2_str:
        logging.error("Location 1 or Location 2 were not provided in the correct format")
        return jsonify({"error": "Location 1 or Location 2 were not provided in the correct format"})

    locations = [tuple(location1), tuple(location2)]

    logging.info("plot_second_pair: %s", plot_second_pair)
    if plot_second_pair:
        location3_str = [request.form.get('location3Name'), request.form.get('location3Lat'), request.form.get('location3Lon')]
        location4_str = [request.form.get('location4Name'), request.form.get('location4Lat'), request.form.get('location4Lon')]

        location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
        location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]

        if None in location3 or None in location4 or "" in location3_str or "" in location4_str:
            logging.error("Location 3 or Location 4 were not provided in the correct format")
            return jsonify({"error": "Location 3 or Location 4 were not provided in the correct format"})

        locations.extend([tuple(location3), tuple(location4)])

    try:
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_plate_carree = f"map_image_PlateCarree_{time_str}.png"
        filename_azimuthal_equidistant = f"map_image_AzimuthalEquidistant_{time_str}.png"

        projection = ccrs.PlateCarree()
        generate_map(projection, locations, os.path.join(current_app.root_path, 'images', filename_plate_carree))

        projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
        generate_map(projection, locations, os.path.join(current_app.root_path, 'images', filename_azimuthal_equidistant))

        logging.info("Maps generated")
    except Exception as e:
        logging.exception("Error during map generation: %s", e)
        return jsonify({"error": str(e)})

    return jsonify({
        'filename_plate_carree': url_for('serve_map1', filename=filename_plate_carree),
        'filename_azimuthal_equidistant': url_for('serve_map2', filename=filename_azimuthal_equidistant)
    })

@app.route('/map1/<filename>', methods=['GET'])
def serve_map1(filename):
    image_path = os.path.join(current_app.root_path, 'images', filename)
    return send_file(image_path, mimetype='image/png')

@app.route('/map2/<filename>', methods=['GET'])
def serve_map2(filename):
    image_path = os.path.join(current_app.root_path, 'images', filename)
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
