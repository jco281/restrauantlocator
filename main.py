import requests
import json

API_KEY = 'API_KEY' # Replace with your API key
CITY = '80403'  # Replace with the city you are interested in
SEARCH_RADIUS = 20000  # Radius in meters
TYPE = 'restaurant'  # We are searching for restaurants


def get_location(city):
    geocode_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={API_KEY}'
    response = requests.get(geocode_url)
    results = response.json().get('results')
    if results:
        location = results[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None


def search_restaurants(lat, lng, radius, type):
    places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={API_KEY}'
    response = requests.get(places_url)
    return response.json()


def get_details(place_id):
    details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}'
    response = requests.get(details_url)
    return response.json()


def main():
    lat, lng = get_location(CITY)
    if lat and lng:
        places_result = search_restaurants(lat, lng, SEARCH_RADIUS, TYPE)
        if 'results' in places_result:
            for place in places_result['results']:
                place_id = place['place_id']
                details = get_details(place_id)
                if 'result' in details:
                    result = details['result']
                    name = result.get('name')
                    address = result.get('formatted_address')
                    phone_number = result.get('formatted_phone_number')
                    website = result.get('website')

                    print(f"Name: {name}")
                    print(f"Address: {address}")
                    print(f"Phone Number: {phone_number}")
                    if website:
                        print(f"Website: {website}")
                    else:
                        print("Website: Not available")
                    print("-" * 40)
        else:
            print("No results found.")
    else:
        print("Location not found.")


if __name__ == "__main__":
    main()
