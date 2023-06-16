from flask import Flask, render_template, request
import logging
import os
import great_circle_v2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    filename_plate_carree = 'blank_plate_carree.png'
    filename_azimuthal_equidistant = 'blank_azimuthal_equidistant.png'
    
    location1_str = ["", "", ""]
    location2_str = ["", "", ""]
    location3_str = ["", "", ""]
    location4_str = ["", "", ""]
    
    plot_first_pair = False
    plot_second_pair = True
    
    if request.method == 'POST':
        location1_str = [request.form.get('location1Name', ''), 
                         request.form.get('location1Lat', ''), 
                         request.form.get('location1Lon', '')]
        location2_str = [request.form.get('location2Name', ''), 
                         request.form.get('location2Lat', ''), 
                         request.form.get('location2Lon', '')]
        location3_str = [request.form.get('location3Name', ''), 
                         request.form.get('location3Lat', ''), 
                         request.form.get('location3Lon', '')]
        location4_str = [request.form.get('location4Name', ''), 
                         request.form.get('location4Lat', ''), 
                         request.form.get('location4Lon', '')]

        plot_first_pair = 'plotFirstPair' in request.form
        plot_second_pair = 'plotSecondPair' in request.form
        
        location1 = [location1_str[0], convert_coord(location1_str[1]), convert_coord(location1_str[2])]
        location2 = [location2_str[0], convert_coord(location2_str[1]), convert_coord(location2_str[2])]
        location3 = [location3_str[0], convert_coord(location3_str[1]), convert_coord(location3_str[2])]
        location4 = [location4_str[0], convert_coord(location4_str[1]), convert_coord(location4_str[2])]

        if plot_first_pair:
            if None in location1 or None in location2 or "" in location1_str or ""
