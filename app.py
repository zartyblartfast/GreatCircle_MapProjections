from flask import Flask, render_template, request, send_file, jsonify, current_app
import os
from map_generator import main as generate_map
import cartopy.crs as ccrs
import traceback
import logging
from datetime import datetime

logging.basicConfig(filename='/home/zartyblartfast/GreatCircle_MapProjections/app.log', level=logging.DEBUG)

app = Flask(__name__)

def convert_coord(coord_str):
    try:
        if coord_str[-1].upper() in ('N', 'S', 'E', 'W'):
            direction = coord_str[-1].upper()
            coord = float(coord_str[:-1])
            if direction in ('S', 'W'):
                coord *= -1  # Switch to negative for S and W
        else:
            coord = float(coord_str)
    except ValueError:
        return None
    return coord

@app.route('/', methods=['GET', 'POST'])
def index():
    location1_str = ["", "", ""]
    location2_str = ["", "", ""]
    location3_str = ["", "", ""]
    location4_str = ["", "", ""]

    plot_second_pair = False

    return render_template('index.html',
                       filename_plate_carree=None,
                       filename_azimuthal_equidistant=None,
                       location1=location1_str,
                       location2=location2_str,
                       location3=location3_str if plot_second_pair else ["", "", ""],
                       location4=location4_str if plot_second_pair else ["", "", ""],
                       plot_second_pair=plot_second_pair)

@app.route('/generate_map', methods=['POST'])
def generate_map_ajax():
    filename_plate_carree = None
    filename_azimuthal_equidistant = None

    location1_str = [request.form.get('location1Name'), request.form.get('location1Lat'), request.form.get('location1Lon')]
    location2_str = [request.form.get('location2Name'), request.form.get('location2Lat'), request.form.get('location2Lon')]

    plot_second_pair = 'plotSecondPair' in request.form

    location1 = location2 = location3 = location4 = None
    
    if not ("" in location1_str):
        location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
    if not ("" in location2_str):
        location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]
    
    if location1 and location2 and None not in location1 and None not in location2:
        locations = [tuple(location1), tuple(location2)]
    else:
        locations = []
    
    if plot_second_pair:
        location3_str = [request.form.get('location3Name'), request.form.get('location3Lat'), request.form.get('location3Lon')]
        location4_str = [request.form.get('location4Name'), request.form.get('location4Lat'), request.form.get('location4Lon')]
        
        if not ("" in location3_str):
            location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
        if not ("" in location4_str):
            location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]
    
        if location3 and location4 and None not in location3 and None not in location4:
            locations.extend([tuple(location3), tuple(location4)])
    
    if not locations:
        return jsonify({"error": "No locations provided."})

    try:
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_plate_carree = f"map_image_PlateCarree_{time_str}.png"
        filename_azimuthal_equidistant = f"map_image_AzimuthalEquidistant_{time_str}.png"

        projection = ccrs.PlateCarree()
        logging.info("PlateCarree map file path: %s", current_app.root_path)
        logging.info("PlateCarree image path: %s", os.path.join(current_app.root_path, 'images', filename_plate_carree))
        generate_map(projection, locations, os.path.join(current_app.root_path, 'images', filename_plate_carree))

        projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
        logging.info("AzimuthalEquidistant map file path: %s", current_app.root_path)
        logging.info("AzimuthalEquidistant image path: %s", os.path.join(current_app.root_path, 'images', filename_azimuthal_equidistant))
        generate_map(projection, locations, os.path.join(current_app.root_path, 'images', filename_azimuthal_equidistant))

        logging.info("Maps generated")
    except Exception as e:
        logging.exception("Error during map generation: %s", e)
        return jsonify({"error": str(e)})

    return jsonify({
        'filename_plate_carree': filename_plate_carree,
        'filename_azimuthal_equidistant': filename_azimuthal_equidistant
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
