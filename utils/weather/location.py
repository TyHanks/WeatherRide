import geocoder

#********************************************************#
#* CLASS *# IP/ Longitude, Latitude Geocoder 
#********************************************************#
def get_location():
    g = geocoder.ip('me')
    currentlocation = g.latlng
    lon = currentlocation[0]
    lat = currentlocation[1]
    country = g.country

    return lon, lat, country