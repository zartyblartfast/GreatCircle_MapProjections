from flask import Flask, render_template, request, send_file
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
    filename_plate_carree = "default_PlateCarree.png"
    filename_azimuthal_equidistant = "default_AzimuthalEquidistant.png"

    location1_str = ["", "", ""]
    location2_str = ["", "", ""]
    location3_str = ["", "", ""]
    location4_str = ["", "", ""]

    include_first_pair = False
    include_second_pair = False

    if request.method == 'POST':
        logging.info('Received POST request')

        # Check if the checkboxes are selected
        include_first_pair = 'includeFirstPair' in request.form
        include_second_pair = 'includeSecondPair' in request.form

        if include_first_pair:
            location1_str = [request.form.get('location1Name'), request.form.get('location1Lat'), request.form.get('location1Lon')]
            location2_str = [request.form.get('location2Name'), request.form.get('location2Lat'), request.form.get('location2Lon')]

            location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
            location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]

            if None in location1 or None in location2 or "" in location1_str or "" in location2_str:
                logging.error("Location 1 or Location 2 were not provided in correct format")
                return "Location 1 or Location 2 were not provided in correct format"
        
        if include_second_pair:
            location3_str = [request.form.get('location3Name'), request.form.get('location3Lat'), request.form.get('location3Lon')]
            location4_str = [request.form.get('location4Name'), request.form.get('location4Lat'), request.form.get('location4Lon')]

            location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
            location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]

            if None in location3 or None in location4 or "" in location3_str or "" in location4_str:
                logging.error("Location 3 or Location 4 were not provided in correct format")
                return "Location 3 or Location 4 were not provided in correct format"
        
        locations = []
        if include_first_pair:
            locations.extend([tuple(location1), tuple(location2)])

        if include_second_pair:
            locations.extend([tuple(location3), tuple(location4)])

        try:
            filename_plate_carree = datetime.now().strftime("%Y%m%d_%H%M%S_PlateCarree.png")
            generate_map(locations, filename_plate_carree, ccrs.PlateCarree())
            
            filename_azimuthal_equidistant = datetime.now().strftime("%Y%m%d_%H%M%S_AzimuthalEquidistant.png")
            generate_map(locations, filename_azimuthal_equidistant, ccrs.AzimuthalEquidistant())
            
        except Exception as e:
            logging.error("Error occurred while generating maps")
            logging.error(traceback.format_exc())
            return "Error occurred while generating maps"

    return os.getcwd() + '<br>' + render_template('index.html', 
                                                  filename_plate_carree=filename_plate_carree, 
                                                  filename_azimuthal_equidistant=filename_azimuthal_equidistant,
                                                  location1=location1_str,
                                                  location2=location2_str,
                                                  location3=location3_str,
                                                  location4=location4_str,
                                                  includeFirstPair=include_first_pair,
                                                  includeSecondPair=include_second_pair)

@app.route('/map/<filename>')
def serve_map(filename):
    return send_file(os.path.join(os.getcwd(), filename), mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
