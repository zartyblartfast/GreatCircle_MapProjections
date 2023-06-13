from flask import Flask, render_template, request, send_file
import os
from map_generator import main as generate_map
import cartopy.crs as ccrs
import traceback

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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
        if projection == 'PlateCarree':
            projection = ccrs.PlateCarree()
        elif projection == 'AzimuthalEquidistant':
            projection = ccrs.AzimuthalEquidistant(central_latitude=90, central_longitude=0)
        
        # Generate the map
        try:
            generate_map(projection, locations)
        except Exception as e:
            with open("/home/zartyblartfast/error_log.txt", "a") as file:
                file.write(f"Error in map generation: {e}\n")
                file.write(f"Traceback: {traceback.format_exc()}\n")

        
        # Serve the generated map to the user
        image_path = os.path.join('/home/zartyblartfast/GreatCircle_MapProjections', 'map_image.png')
        return send_file(image_path, mimetype='image/png')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
