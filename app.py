from flask import Flask, render_template, request, send_file
import os
from map_generator import main as generate_map
import cartopy.crs as ccrs
import traceback
import logging

logging.basicConfig(filename='/home/zartyblartfast/GreatCircle_MapProjections/app.log', level=logging.DEBUG)

app = Flask(__name__)

def convert_coord(coord_str):
    if not coord_str[-1].upper() in ('N', 'S', 'E', 'W'):
        return None
    direction = coord_str[-1].upper()
    coord = float(coord_str[:-1])
    if direction in ('S', 'W'):
        coord *= -1  # Switch to negative for S and W
    return coord

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.info('Received POST request')

        # Get user input
        location1_str = [request.form.get('location1Name'), request.form.get('location1Lat'), request.form.get('location1Lon')]
        location2_str = [request.form.get('location2Name'), request.form.get('location2Lat'), request.form.get('location2Lon')]
        location3_str = [request.form.get('location3Name'), request.form.get('location3Lat'), request.form.get('location3Lon')]
        location4_str = [request.form.get('location4Name'), request.form.get('location4Lat'), request.form.get('location4Lon')]

        location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
        location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]

        if None in location1 or None in location2:
            return "Location 1 or Location 2 were not provided in correct format"

        location3 = None
        location4 = None
        if location3_str[0] and location3_str[1] and location4_str[0] and location4_str[1]:
            location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
            location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]

        # Process user input
        locations = [tuple(location1), tuple(location2)]
        if location3 and location4:
            locations.extend([tuple(location3), tuple(location4)])

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
