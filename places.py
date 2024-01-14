import requests
import pickle
from restaurant_reviews import Restaurant
from redis_cloud_db import connect_to_redis, add_reviews, get_reviews2, search

API_KEY = 'AIzaSyC4NvunD89s_xmgUUvV59EhX0dGO-zKnbM'

def get_reviews(restaurant):
    place_id = get_place_id(restaurant.name, restaurant.location)

    if place_id:
        reviews = get_reviews_text_by_place_id(place_id)
        return reviews
    else:
        return None

def get_place_id(restaurant_name, location):
    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={restaurant_name} {location}&inputtype=textquery&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'candidates' in data and data['candidates']:
        return data['candidates'][0]['place_id']
    else:
        return None

def get_reviews_text_by_place_id(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and 'result' in data and 'reviews' in data['result']:
        reviews_data = data['result']['reviews'][:10]
        review_texts = [review['text'] for review in reviews_data]
        return review_texts
    else:
        return None


def get_location_from_postal_code(postal_code, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{postal_code}, Canada",
        "key": api_key,
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200 and data.get("results"):
        formatted_address = data["results"][0]["formatted_address"]
        return formatted_address
    else:
        return f"Location not found for postal code {postal_code}"

def main_get_total_reviews(restaurant_name, postal_code):
    # Input: Name of the restaurant and postal code
    #restaurant_name = 'Pita N More'
    #postal_code = 'L8S 1C5'

    # Get location from postal code
    location = get_location_from_postal_code(postal_code, API_KEY)

    # Create a Restaurant instance
    restaurant = Restaurant(restaurant_name, postal_code, location)

    # Connect to Redis
    redis_conn = connect_to_redis()

    # Check if restaurant exists in the database
    if search(redis_conn, postal_code):
        # If yes, get reviews from the database
        reviews_from_db = get_reviews2(redis_conn, postal_code)
        restaurant.reviews.extend(reviews_from_db)
        return restaurant.reviews

    # Get reviews from Places API
    reviews_from_places = get_reviews(restaurant)

    if reviews_from_places:
        # Add reviews to the database
        add_reviews(redis_conn, postal_code, reviews_from_places)

        # Add reviews to the restaurant instance
        restaurant.reviews.extend(reviews_from_places)

    return restaurant.reviews
if __name__ == "__main__":
    main_get_total_reviews("McDonald's", "L6X 0B3")
    main_get_total_reviews("Popeyes", 'L6Y 6A1')
    main_get_total_reviews('Pita N More','L8S 1C5' )
