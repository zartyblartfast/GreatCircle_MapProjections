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
        location1 = request.form.get('location1').split(',')
        location2 = request.form.get('location2').split(',')
        location3 = request.form.get('location3').split(',')
        location4 = request.form.get('location4').split(',')
        
        # Process user input
        locations = [
            (location1[0], float(location1[1]), float(location1[2])),
            (location2[0], float(location2[1]), float(location2[2])),
            (location3[0], float(location3[1]), float(location3[2])),
            (location4[0], float(location4[1]), float(location4[2])),
        ]
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
