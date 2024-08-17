import requests
from city_api.settings import OPENCAGE_API_KEY


def get_city_coordinates(city_name):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={OPENCAGE_API_KEY}&limit=1'

    response = requests.get(url)
    data = response.json()

    if data['results']:
        latitude = data['results'][0]['geometry']['lat']
        longitude = data['results'][0]['geometry']['lng']
        return latitude, longitude

    raise ValueError("Couldn't fetch coordinates for the city.")
