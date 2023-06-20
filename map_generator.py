import logging_config

logging_config.setup_logger()

import os
import numpy as np
import matplotlib.pyplot as plt
import pyproj
import cartopy.crs as ccrs
import cartopy.mpl.gridliner as cgridliner
import matplotlib.ticker as mticker
from matplotlib import transforms as mtransforms
import logging

# Get a logger instance
logger = logging.getLogger(__name__)

def calculate_great_circle_points(lon1, lat1, lon2, lat2, num_points):
    logger.info(f"Calculating great circle points between ({lon1}, {lat1}) and ({lon2}, {lat2}) with {num_points} points")
    g = pyproj.Geod(ellps='WGS84')
    lonlats = np.array(g.npts(lon1, lat1, lon2, lat2, num_points))
    lonlats = np.vstack([[lon1, lat1], lonlats, [lon2, lat2]])  # Add start and end points
    return lonlats

def plot_great_circle(lonlats, ax, color='b', linewidth=2, zorder=3):
    logger.info(f"Plotting great circle for {len(lonlats)} points")
    
    ax.plot(lonlats[:,0], lonlats[:,1], color, transform=ccrs.Geodetic(), linewidth=linewidth, zorder=zorder)
    
    # Calculate the great circle distance
    g = pyproj.Geod(ellps='WGS84')
    lon1, lat1 = lonlats[0]
    lon2, lat2 = lonlats[-1]
    az12, az21, dist = g.inv(lon1, lat1, lon2, lat2)
    dist_km = dist/1000  # convert from meters to kilometers
    
    # Add distance text in the center of the line
    center_index = len(lonlats) // 2
    text_lon, text_lat = lonlats[center_index]
    
    # Small adjustments to the text coordinates to offset the text
    text_lon += 5
    text_lat += 5
    
    ax.text(text_lon, text_lat, f"{dist_km:.0f} km", transform=ccrs.Geodetic(), fontsize=10, ha='right', va='bottom', color=color)

    return color  # Return the color code

def plot_location_point(name, lon, lat, ax, color='r'):
    logger.info(f"Plotting location point for {name} at ({lon}, {lat})")
    
    ax.plot(lon, lat, 'o', transform=ccrs.Geodetic(), color=color, markersize=7)
    ax.text(lon, lat, name, transform=ccrs.Geodetic(), fontsize=10, ha='right', va='bottom', color=color)

    return color  # Return the color code

def main(projection, locations, output_file):
    logger.info(f"Generating map with projection {projection}, {len(locations)} locations, and output file {output_file}")

    No_Locations = False
    
    # Unpack the location details
    if len(locations) == 2:
        location1, location2 = locations
        location3 = location4 = None
    elif len(locations) == 4:
        location1, location2, location3, location4 = locations
    else:
        #logger.error("locations must have length 2 or 4")
        #raise ValueError("locations must have length 2 or 4")
        No_Locations = True

    if No_Locations == False:
        # Calculate the great circle points
        lonlats1 = calculate_great_circle_points(location1[2], location1[1], location2[2], location2[1], 2000)
        
        if location3 and location4:
            lonlats2 = calculate_great_circle_points(location3[2], location3[1], location4[2], location4[1], 2000)

    # Create the map
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=projection)

    ax.stock_img()

    # Plot the great circles and get their colors
    color1 = plot_great_circle(lonlats1, ax, color='b', linewidth=2, zorder=3)

    if No_Locations == False:
        if location3 and location4:
            color2 = plot_great_circle(lonlats2, ax, color='r', linewidth=2, zorder=3)
    
        # Plot the location points
        plot_location_point(location1[0], location1[2], location1[1], ax, color=color1)
        plot_location_point(location2[0], location2[2], location2[1], ax, color=color1)
        
        if location3 and location4:
            plot_location_point(location3[0], location3[2], location3[1], ax, color=color2)
            plot_location_point(location4[0], location4[2], location4[1], ax, color=color2)

    ax.set_global()

    # Add gridlines
    if isinstance(projection, ccrs.PlateCarree):
        gl = ax.gridlines(crs=projection, draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
        gl.top_labels = False
        gl.right_labels = False
        gl.xlines = True
        gl.xlocator = mticker.FixedLocator([-180, -120, -60, 0, 60, 120, 180])
        gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0, 30, 60, 90])
    elif isinstance(projection, ccrs.AzimuthalEquidistant):
        gl = ax.gridlines(draw_labels=True)  # You might want to exclude labels in Azimuthal projection
        gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))
        gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 30))

    try:
        plt.savefig(output_file)
        logger.info(f"Map successfully saved to {output_file}")
    except Exception as e:
        logger.exception("Failed to save map")
        raise ValueError("Failed to save map")
        
    # Close the figure to free up memory
    plt.close(fig)
