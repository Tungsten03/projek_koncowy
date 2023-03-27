from geopy import geocoders
geolocator = geocoders.Nominatim(user_agent='lokacja')
location = geolocator.geocode('Poznań, Collegium Da Vinci')
koordy1  = (location.latitude, location.longitude)
print(koordy1)
koordy = geolocator.reverse('52.41579805, 16.931231975777052')
print(koordy.address)
