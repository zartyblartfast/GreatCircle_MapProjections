import numpy as np
import matplotlib.pyplot as plt
import pyproj
import cartopy.crs as ccrs
import cartopy.mpl.gridliner as cgridliner
import matplotlib.ticker as mticker
from matplotlib import transforms as mtransforms

def calculate_great_circle_points(lon1, lat1, lon2, lat2, num_points):
    g = pyproj.Geod(ellps='WGS84')
    lonlats = np.array(g.npts(lon1, lat1, lon2, lat2, num_points))
    lonlats = np.vstack([[lon1, lat1], lonlats, [lon2, lat2]])  # Add start and end points
    return lonlats

def plot_great_circle(lonlats, ax, color='b', linewidth=2, zorder=3):
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
    ax.plot(lon, lat, 'o', transform=ccrs.Geodetic(), color=color, markersize=7)
    ax.text(lon, lat, name, transform=ccrs.Geodetic(), fontsize=10, ha='right', va='bottom', color=color)

    return color  # Return the color code

def main(projection, locations):
    # Unpack the location details
    location1, location2, location3, location4 = locations

    # Calculate the great circle points
    lonlats1 = calculate_great_circle_points(location1[2], location1[1], location2[2], location2[1], 2000)
    lonlats2 = calculate_great_circle_points(location3[2], location3[1], location4[2], location4[1], 2000)

    # Create the map
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=projection)

    ax.stock_img()

    # Plot the great circles and get their colors
    color1 = plot_great_circle(lonlats1, ax, color='b', linewidth=2, zorder=3)
    color2 = plot_great_circle(lonlats2, ax, color='r', linewidth=2, zorder=3)

    # Plot the location points
    plot_location_point(location1[0], location1[2], location1[1], ax, color=color1)
    plot_location_point(location2[0], location2[2], location2[1], ax, color=color1)
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
        gl.ylocator = mticker.FixedLocator(np.arange(-90, 120, 30))
        # Manually add labels
        for lat in np.arange(-90, 91, 30):
            ax.annotate(str(lat), xy=(0, lat), xycoords=ccrs.PlateCarree()._as_mpl_transform(ax), fontsize=10)

    #plt.savefig("map_image.png")  # Save the generated map as a PNG image
    plt.savefig("/home/zartyblartfast/GreatCircle_MapProjections/map_image.png")

    #test
    with open('/home/zartyblartfast/map_generator_test.txt', 'w') as f:
    f.write("Map generator test.")

    plt.close(fig)  # Close the figure to free up memory

if __name__ == "__main__":
    location1 = ('Tokyo_HND', 35.5494, 139.7798)
    location2 = ('London_LHR', 51.4700, -0.4543)
    location3 = ('Cape_Town_CPT', -33.9715, 18.6021)
    location4 = ('Hobart_HBA', -42.8364, 147.5075)
    locations = [location1, location2, location3, location4]
    projection = ccrs.PlateCarree()  # Replace this with the actual projection
    main(projection, locations)
