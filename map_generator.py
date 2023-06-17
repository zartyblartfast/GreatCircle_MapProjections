import numpy as np
import matplotlib.pyplot as plt
import pyproj
import cartopy.crs as ccrs
import cartopy.mpl.gridliner as cgridliner
import matplotlib.ticker as mticker

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

def main(projection, locations, output_file):
    if len(locations) != 2 and len(locations) != 4:
        raise ValueError("locations must have length 2 or 4")

    # Calculate the great circle points
    lonlats1 = calculate_great_circle_points(locations[0][2], locations[0][1], locations[1][2], locations[1][1], 2000)
    
    if len(locations) == 4:
        lonlats2 = calculate_great_circle_points(locations[2][2], locations[2][1], locations[3][2], locations[3][1], 2000)

    # Create the map
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=projection)

    ax.stock_img()

    # Plot the great circles and get their colors
    color1 = plot_great_circle(lonlats1, ax, color='b', linewidth=2, zorder=3)
    
    if len(locations) == 4:
        color2 = plot_great_circle(lonlats2, ax, color='r', linewidth=2, zorder=3)

    # Plot the location points
    plot_location_point(locations[0][0], locations[0][2], locations[0][1], ax, color=color1)
    plot_location_point(locations[1][0], locations[1][2], locations[1][1], ax, color=color1)
    
    if len(locations) == 4:
        plot_location_point(locations[2][0], locations[2][2], locations[2][1], ax, color=color2)
        plot_location_point(locations[3][0], locations[3][2], locations[3][1], ax, color=color2)

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

    plt.savefig(output_file)

    # Close the figure to free up memory
    plt.close(fig)
