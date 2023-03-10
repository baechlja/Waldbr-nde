import gmplot
from math import asin, atan2, cos, degrees, radians, sin
from weather import get_wind_dir, get_wind_bft
import os
import webbrowser


# FUNCTIONS

def get_point_at_distance(lat1, lon1, d, bearing, R=6371):
    """
    lat: initial latitude, in degrees
    lon: initial longitude, in degrees
    d: target distance from initial
    bearing: (true) heading in degrees
    R: optional radius of sphere, defaults to mean radius of earth

    Returns new lat/lon coordinate {d}km from initial, in degrees
    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    a = radians(bearing)
    lat2 = asin(sin(lat1) * cos(d/R) + cos(lat1) * sin(d/R) * cos(a))
    lon2 = lon1 + atan2(
        sin(a) * sin(d/R) * cos(lat1),
        cos(d/R) - sin(lat1) * sin(lat2)
    )
    return (degrees(lat2), degrees(lon2),)

def heatmap(api_key,lat,lon,fire_geo=None,fire_station=None,weights=None):
    """
    api_key: key for OpenWeatherMap
    lat: initial latitude
    lon: initial longitude
    fire_geo: list object with tupel of lat and long of fire spots
    weight: list object with same size like fire_geo, includes fire intensity of the spot. Default None

    Returns a map with current fire as heatpoints
    """
    # LOCATION
    map = gmplot.GoogleMapPlotter(lat, lon, 14.5) 
    map.apikey = "XXX"

    # FIRE SPOTS
    #add heatmap
    if fire_geo != None:
        lats, longs = zip(*fire_geo)
        
        map.heatmap(lats, longs,radius=20, weights= weights)
        path = fire_geo + fire_station
        path_lats, path_longs = zip(*path)
        map.plot(path_lats, path_longs, "cornflowerblue", edge_width=3.0)
        fire_lat, fire_lon = zip(*fire_station)
        
        map.scatter(fire_lat, fire_lon, marker=True,size=100,color='red', label='Firestation')

        #WIND
        #add Scatter in Wind direction
        scatter = []
        #add Scatter in color of Wind speed green is low and red is high
        wind_speed = []
        wind_color = {0: 'lightgreen', 1: 'forestgreen', 2: 'deepskyblue', 3: 'royalblue', 4: 'navy',
                    5: 'blueviolet', 6: 'indigo', 7: 'purple', 8: 'darkmagenta', 9: 'crimson', 10: 'red', 
                    11: 'darkred', 12: 'maroon'}
        #loop over fire spots
        for n in fire_geo:
            #get wind degree from weather script
            wind = get_wind_dir(api_key,n[0], n[1])
            #get wind speed in bft from weather script
            bft = get_wind_bft(api_key,n[0], n[1])
            #append speed to list
            wind_speed.append(bft)
            #get centre of the scatter 
            lat, lon = get_point_at_distance(n[0], n[1],0.05,wind)
            #append each center point to list
            scatter.append((lat,lon))
        #unzip to add it to gmplot.scatter soon    
        slats, slongs = zip(*scatter)
        #get wind colors from dictonary
        colors = [wind_color[x] for x in wind_speed]
        #plot scatters
        map.scatter(slats, slongs, colors, marker=False, symbol='o', size= 100, alpha=0.4)
        #map.text(lat, lon + 0.02, 'Wind:' + str(set([wind_type[x] for x in wind_speed])))
        #plot whole map
    map.draw( "fire.html" )

# TESTING
# Loerrach:

# loe_lat = 47.6169
# loe_lon = 7.6709
# fire_geo = [
#         (47.6170, 7.6709), (47.6270, 7.6710), (47.6188, 7.6709),
#         (47.6169, 7.6758)]


# heatmap(loe_lat,loe_lon,fire_geo)

# Freiburg:

# fr_lat = 47.997791
# fr_lon = 7.842609
# fire_spots = [
#         (47.998891, 7.842609), (47.994791, 7.843609)]

# heatmap(fr_lat,fr_lon,fire_spots)