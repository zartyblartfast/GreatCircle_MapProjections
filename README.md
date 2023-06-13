# Display Great Circles on Two Different Map Projections

## Project Description

This web application is designed to help users understand the concept of great circles and map projections. It enables users to input two pairs of geographical coordinates (latitude and longitude) and then generates maps that display the great circles - the shortest path between two points on a sphere's surface - connecting these points. The maps are rendered in two different map projections to demonstrate the distortion inherent in 2D representations of a sphere's surface.

## How to Use

To use this web application, enter the latitude and longitude for two locations in the form fields provided. If desired, you can also input a second pair of locations. Once you have entered the locations, click on the "Generate Maps" button. The application will then generate two maps displaying the great circles between the locations in two different map projections.

There are several optional features that you can toggle on or off:

- **Gridlines**: Display gridlines and latitude/longitude labels on the maps.
- **Location Labels**: Display labels for the input locations on the maps.
- **Distance Labels**: Display labels for the distance of the great circles on the maps.

By default, all of these options are turned on.

## Installation

This application is web-based and does not require installation. You can access it [here](https://github.com/zartyblartfast/GreatCircle_MapProjections). To use it, you need a modern web browser such as Google Chrome, Firefox, or Safari.

## Contributing

If you have suggestions for how this project could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For direct contributions, please fork the repository and create your feature branch, then open a PR with your suggested changes.

## Acknowledgements

This project uses the following open-source libraries:

- Flask (Python web framework)
- Pyproj (Python interface to PROJ - cartographic projections and coordinate transformations library)
- Matplotlib (Python 2D plotting library)
- Cartopy (Python package for geospatial data processing and visualization)

## License

This project is open source, under the [MIT License](https://opensource.org/licenses/MIT).

