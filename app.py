from flask import Flask, render_template, request, send_file
import os
from map_generator import main as generate_map
import cartopy.crs as ccrs
import traceback
import logging

logging.basicConfig(filename='/home/zartyblartfast/GreatCircle_MapProjections/app.log', level=logging.DEBUG)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.info('Received POST request')

        # Get user input
        location1_str = request.form.get('location1Lat') + request.form.get('location1Lon')
        location2_str = request.form.get('location2Lat') + request.form.get('location2Lon')
        location3_str = request.form.get('location3Lat') + request.form.get('location3Lon')
        location4_str = request.form.get('location4Lat') + request.form.get('location4Lon')

        # Check for None values
        if location1_str is None or location2_str is None:
            return "Location 1 or Location 2 were not provided"

        location1 = location1_str.split(',')
        location2 = location2_str.split(',')
        location3 = None
        location4 = None

        if location3_str is not None and location4_str is not None:
            location3 = location3_str.split(',')
            location4 = location4_str.split(',')
        
        # Process user input
        locations = [
            (location1[0], float(location1[1]), float(location1[2])),
            (location2[0], float(location2[1]), float(location2[2])),
        ]
        if location3 is not None and location4 is not None:
            locations.append(
                (location3[0], float(location3[1]), float(location3[2])),
                (location4[0], float(location4[1]), float(location4[2])),
            )
        logging.info(f"Locations: {locations}")

        try:
            # For the first projection (PlateCarree)
            projection = ccrs.PlateCarree()
            generate_map(projection, locations, "map_image_PlateCarree.png")

            # For the second projection (AzimuthalEquidistant)
            projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
            generate_map(projection, locations, "map_image_AzimuthalEquidistant.png")

            logging.info("Maps generated")
        except Exception as e:
            logging.info("Error during map generation: %s", e)
            return str(e)
        
        logging.info("After map generation")

    # Add this line to print the current working directory to the webpage
    return os.getcwd() + '<br>' + render_template('index.html')

@app.route('/map1', methods=['GET'])
def serve_map1():
    image_path = os.path.join('/home/zartyblartfast/GreatCircle_MapProjections', 'map_image_PlateCarree.png')
    return send_file(image_path, mimetype='image/png')

@app.route('/map2', methods=['GET'])
def serve_map2():
    image_path = os.path.join('/home/zartyblartfast/GreatCircle_MapProjections', 'map_image_AzimuthalEquidistant.png')
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
