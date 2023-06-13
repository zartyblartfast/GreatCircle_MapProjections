from flask import Flask, render_template, request
import your_script_name  # Import your script here.

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        projection_type = request.form.get('projectionType')  # Replace 'projectionType' with the actual name of the form input for the map projection.
        location1_name = request.form.get('location1Name')
        location1_lat = request.form.get('location1Lat')
        location1_long = request.form.get('location1Long')
        # Repeat for location 2.

        # Use these variables as arguments for a function in your script that generates and saves the map image.
        your_script_name.main(projection_type, location1_name, location1_lat, location1_long)  # Replace 'main' with the actual name of the function.

        return 'Map image generated.'  # Replace this with code to display the image on the webpage.

    else:
        return render_template('index.html')
