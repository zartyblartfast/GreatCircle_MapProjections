import logging_config

logging_config.setup_logger()

from flask import Flask, render_template, request, send_file, jsonify
import os
import json
from map_generator import main as generate_map
import cartopy.crs as ccrs
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

app = Flask(__name__)

if not app.debug:
    file_handler = RotatingFileHandler(filename=os.path.join('/home/zartyblartfast/GreatCircle_MapProjections', 'app.log'), maxBytes=1024*1024*10, backupCount=0)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
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
        return render_template('index.html',
                               filename_plate_carree=None,
                               filename_azimuthal_equidistant=None,
                               location1=["", "", ""],
                               location2=["", "", ""],
                               location3=["", "", ""],
                               location4=["", "", ""],
                               plot_second_pair=False,
                               location_data=location_data)

@app.route('/generate_map', methods=['POST'])
def generate_map_ajax():
    filename_plate_carree = None
    filename_azimuthal_equidistant = None

    plot_first_pair = 'plotFirstPair' in request.form
    plot_second_pair = 'plotSecondPair' in request.form

    if not plot_first_pair and not plot_second_pair:
        # If neither checkbox is checked, generate empty maps
        try:
            time_str = datetime.now().strftime("%Y%m%d%H%M%S")
            filename_plate_carree = f"map_image_PlateCarree_{time_str}.png"
            filename_azimuthal_equidistant = f"map_image_AzimuthalEquidistant_{time_str}.png"

            folderPath_plate_carree = os.path.join(app.root_path, 'static', 'images', filename_plate_carree)
            folderPath__azimuthal_equidistant = os.path.join(app.root_path, 'static', 'images', filename_azimuthal_equidistant)

            # Generate maps with no locations
            generate_map(ccrs.PlateCarree(), [], folderPath_plate_carree)
            generate_map(ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0), [], folderPath__azimuthal_equidistant)
        except Exception as e:
            app.logger.error("Error during map generation: %s", e)
            return jsonify({"error": str(e)})

        return jsonify({
            'filename_plate_carree': filename_plate_carree,
            'filename_azimuthal_equidistant': filename_azimuthal_equidistant
        })

    location1_str = [request.form.get('location1Name'), request.form.get('latitude1'), request.form.get('longitude1')]
    app.logger.info(f"Received location1 data: {location1_str}")
    location2_str = [request.form.get('location2Name'), request.form.get('latitude2'), request.form.get('longitude2')]
    app.logger.info(f"Received location2 data: {location2_str}")

    app.logger.info(f"Form data: {request.form}")

    locations = []

    if plot_first_pair:
        location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
        location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]
        
        if None in location1 or None in location2 or "" in location1_str or "" in location2_str:
            app.logger.error("Location 1 or Location 2 were not provided in the correct format")
            return jsonify({"error": "Location 1 or Location 2 were not provided in the correct format"})
        
        locations.extend([tuple(location1), tuple(location2)])

    if plot_second_pair:
        location3_str = [request.form.get('location3Name'), request.form.get('latitude3'), request.form.get('longitude3')]
        app.logger.info(f"Received location3 data: {location3_str}")
        location4_str = [request.form.get('location4Name'), request.form.get('latitude4'), request.form.get('longitude4')]
        app.logger.info(f"Received location4 data: {location4_str}")
        
        location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
        location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]

        if None in location3 or None in location4 or "" in location3_str or "" in location4_str:
            app.logger.error("Location 3 or Location 4 were not provided in the correct format")
            return jsonify({"error": "Location 3 or Location 4 were not provided in the correct format"})

        locations.extend([tuple(location3), tuple(location4)])

    try:
        time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        filename_plate_carree = f"map_image_PlateCarree_{time_str}.png"
        filename_azimuthal_equidistant = f"map_image_AzimuthalEquidistant_{time_str}.png"

        folderPath_plate_carree = os.path.join(app.root_path, 'static', 'images', filename_plate_carree)
        folderPath__azimuthal_equidistant = os.path.join(app.root_path, 'static', 'images', filename_azimuthal_equidistant)

        projection = ccrs.PlateCarree()
        app.logger.info("folderPath_plate_carree: %s", folderPath_plate_carree)
        app.logger.info("filename_plate_carree: %s", filename_plate_carree)
        generate_map(projection, locations,folderPath_plate_carree)

        projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
        app.logger.info("folderPath__azimuthal_equidistant: %s", folderPath__azimuthal_equidistant)
        app.logger.info("filename_azimuthal_equidistant: %s", filename_azimuthal_equidistant)
        generate_map(projection, locations,folderPath__azimuthal_equidistant)

        app.logger.info("Maps generated")
    except Exception as e:
        app.logger.error("Error during map generation: %s", e)
        return jsonify({"error": str(e)})

    return jsonify({
        'filename_plate_carree': filename_plate_carree,
        'filename_azimuthal_equidistant': filename_azimuthal_equidistant
    })

@app.route('/map1/<filename>', methods=['GET'])
def serve_map1(filename):
    image_path = os.path.join(app.root_path, 'static', 'images', filename)
    return send_file(image_path, mimetype='image/png')

@app.route('/map2/<filename>', methods=['GET'])
def serve_map2(filename):
    image_path = os.path.join(app.root_path, 'static', 'images', filename)
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
