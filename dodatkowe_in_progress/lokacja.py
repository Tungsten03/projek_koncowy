from geopy import geocoders
geolocator = geocoders.Nominatim(user_agent='lokacja')
# location = geolocator.geocode('Wrocław, al. Wiśniowa')
# koordy1  = (location.latitude, location.longitude)
# print(koordy1)
# koordy = geolocator.reverse(koordy1)
# print(koordy.address)

def get_coords(station):
    location = geolocator.geocode(station)
    return (location.latitude, location.longitude)