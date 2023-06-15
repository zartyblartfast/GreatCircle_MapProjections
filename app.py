from flask import Flask, render_template, request, send_file
import os
from map_generator import main as generate_map
import cartopy.crs as ccrs
import traceback
import logging
from datetime import datetimefrom flask import Flask, render_template, request, send_file
import os
from map_generator import main as generate_map
import cartopy.crs as ccrs
import traceback
import logging
from datetime import datetime

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
    # Define the variables with default values here
    filename_plate_carree = "default_PlateCarree.png"
    filename_azimuthal_equidistant = "default_AzimuthalEquidistant.png"
    
    if request.method == 'POST':
        logging.info('Received POST request')

        location1_str = [request.form.get('location1Name'), request.form.get('location1Lat'), request.form.get('location1Lon')]
        location2_str = [request.form.get('location2Name'), request.form.get('location2Lat'), request.form.get('location2Lon')]
        plot_second_pair = request.form.get('plotSecondPair')  # New line to fetch checkbox status

        location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
        location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]

        if None in location1 or None in location2:
            return "Location 1 or Location 2 were not provided in correct format"

        locations = [tuple(location1), tuple(location2)]

        # Only fetch and plot the second pair of locations if checkbox is enabled
        if plot_second_pair == 'on':  # New condition for checkbox
            location3_str = [request.form.get('location3Name'), request.form.get('location3Lat'), request.form.get('location3Lon')]
            location4_str = [request.form.get('location4Name'), request.form.get('location4Lat'), request.form.get('location4Lon')]
            
            # Check for non-empty longitude as well for locations 3 and 4
            if location3_str[0] and location3_str[1] and location3_str[2] and location4_str[0] and location4_str[1] and location4_str[2]:
                location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
                location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]
                locations.extend([tuple(location3), tuple(location4)])

        logging.info(f"Locations: {locations}")

        try:
            time_str = datetime.now().strftime("%Y%m%d%H%M%S")
            filename_plate_carree = f"map_image_PlateCarree_{time_str}.png"
            filename_azimuthal_equidistant = f"map_image_AzimuthalEquidistant_{time_str}.png"

            projection = ccrs.PlateCarree()
            generate_map(projection, locations, filename_plate_carree)

            projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
            generate_map(projection, locations, filename_azimuthal_equidistant)

            logging.info("Maps generated")
        except Exception as e:
            logging.info("Error during map generation: %s", e)
            return str(e)
        
        logging.info("After map generation")

        try:
            logging.info(f"Checking if directory exists: {os.path.isdir('/home/zartyblartfast/GreatCircle_MapProjections')}")
            logging.info(f"Checking write access to directory: {os.access('/home/zartyblartfast/GreatCircle_MapProjections', os.W_OK)}")
        except Exception as e:
            logging.error(f"Error during directory checks: {e}")

    return os.getcwd() + '<br>' + render_template('index.html', 
                                                  filename_plate_carree=filename_plate_carree, 
                                                  filename_azimuthal_equidistant=filename_azimuthal_equidistant)

@app.route('/map1/<filename>', methods=['GET'])
def serve_map1(filename):
    image_path = os.path.join('/home/zartyblartfast/', filename)  # Images are generated directly in /home/zartyblartfast/
    return send_file(image_path, mimetype='image/png')

@app.route('/map2/<filename>', methods=['GET'])
def serve_map2(filename):
    image_path = os.path.join('/home/zartyblartfast/', filename)  # Images are generated directly in /home/zartyblartfast/
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)


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
    # Define the variables with default values here
    filename_plate_carree = "default_PlateCarree.png"
    filename_azimuthal_equidistant = "default_AzimuthalEquidistant.png"
    
    if request.method == 'POST':
        logging.info('Received POST request')

        location1_str = [request.form.get('location1Name'), request.form.get('location1Lat'), request.form.get('location1Lon')]
        location2_str = [request.form.get('location2Name'), request.form.get('location2Lat'), request.form.get('location2Lon')]
        plot_second_pair = request.form.get('plotSecondPair')  # New line to fetch checkbox status

        location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
        location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]

        if None in location1 or None in location2:
            return "Location 1 or Location 2 were not provided in correct format"

        locations = [tuple(location1), tuple(location2)]

        # Only fetch and plot the second pair of locations if checkbox is enabled
        if plot_second_pair == 'on':  # New condition for checkbox
            location3_str = [request.form.get('location3Name'), request.form.get('location3Lat'), request.form.get('location3Lon')]
            location4_str = [request.form.get('location4Name'), request.form.get('location4Lat'), request.form.get('location4Lon')]
            
            if location3_str[0] and location3_str[1] and location4_str[0] and location4_str[1]:
                location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
                location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]
                locations.extend([tuple(location3), tuple(location4)])

        logging.info(f"Locations: {locations}")

        try:
            time_str = datetime.now().strftime("%Y%m%d%H%M%S")
            filename_plate_carree = f"map_image_PlateCarree_{time_str}.png"
            filename_azimuthal_equidistant = f"map_image_AzimuthalEquidistant_{time_str}.png"

            projection = ccrs.PlateCarree()
            generate_map(projection, locations, filename_plate_carree)

            projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
            generate_map(projection, locations, filename_azimuthal_equidistant)

            logging.info("Maps generated")
        except Exception as e:
            logging.info("Error during map generation: %s", e)
            return str(e)
        
        logging.info("After map generation")

        try:
            logging.info(f"Checking if directory exists: {os.path.isdir('/home/zartyblartfast/GreatCircle_MapProjections')}")
            logging.info(f"Checking write access to directory: {os.access('/home/zartyblartfast/GreatCircle_MapProjections', os.W_OK)}")
        except Exception as e:
            logging.error(f"Error during directory checks: {e}")

    return os.getcwd() + '<br>' + render_template('index.html', 
                                                  filename_plate_carree=filename_plate_carree, 
                                                  filename_azimuthal_equidistant=filename_azimuthal_equidistant)

@app.route('/map1/<filename>', methods=['GET'])
def serve_map1(filename):
    image_path = os.path.join('/home/zartyblartfast/', filename)  # Images are generated directly in /home/zartyblartfast/
    return send_file(image_path, mimetype='image/png')

@app.route('/map2/<filename>', methods=['GET'])
def serve_map2(filename):
    image_path = os.path.join('/home/zartyblartfast/', filename)  # Images are generated directly in /home/zartyblartfast/
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)

