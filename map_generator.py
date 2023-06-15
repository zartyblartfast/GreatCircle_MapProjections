def main(projection, locations, output_file):
    # Unpack the location details
    if len(locations) == 2:
        location1, location2 = locations
        location3 = location4 = None
    elif len(locations) == 4:
        location1, location2, location3, location4 = locations

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
        gl.xlocator = mticker.FixedLocator(np.arange(-180, 180 and 1 reactions to previous messages in this conversation to keep things tidy.
        gl.xlocator = mticker.FixedLocator(np.arange(-180, 180, 30))
        gl.ylocator = mticker.FixedLocator(np.arange(-90, 90, 30))

    plt.savefig(output_file)

    # Close the figure to free up memory
    plt.close(fig)
