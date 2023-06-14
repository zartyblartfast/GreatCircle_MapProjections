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
        print("POST request received") # added this line
        # Get user input
        location1 = request.form.get('location1').split(',')
        location2 = request.form.get('location2').split(',')
        location3 = request.form.get('location3').split(',')
        location4 = request.form.get('location4').split(',')
        projection = request.form.get('projection')
        
        # Process user input
        locations = [
            (location1[0], float(location1[1]), float(location1[2])),
            (location2[0], float(location2[1]), float(location2[2])),
            (location3[0], float(location3[1]), float(location3[2])),
            (location4[0], float(location4[1]), float(location4[2])),
        ]
        print("Locations:", locations) # added this line
        if projection == 'PlateCarree':
            projection = ccrs.PlateCarree()
        elif projection == 'AzimuthalEquidistant':
            projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
        
        print("Before map generation") # added this line
        try:
            generate_map(projection, locations)
            with open('/home/zartyblartfast/GreatCircle_MapProjections/test.txt', 'w') as f:
                f.write("This is a test.")
        except Exception as e:
            print("Error during map generation:", str(e)) # added this line
            return str(e)
        
        print("After map generation") # added this line
        # Serve the generated map to the user
        image_path = os.path.join('/home/zartyblartfast/GreatCircle_MapProjections', 'map_image.png')
        return send_file(image_path, mimetype='image/png')
        
    # Add this line to print the current working directory to the webpage
    return os.getcwd() + '<br>' + render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)

