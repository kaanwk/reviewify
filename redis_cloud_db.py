import redis
from restaurant_reviews import Restaurant

def connect_to_redis():
    host = 'redis-16849.c321.us-east-1-2.ec2.cloud.redislabs.com'
    port = 16849
    password = 'AJAJV5Wmyq6fTdggRDnjInktlLsubn48'
    r = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
    return r

def add_reviews(redis_conn, postal_code, reviews):
    key = postal_code
    # Check if the key already exists
    if redis_conn.exists(key):
        # Check if the key is of type 'list'
        if redis_conn.type(key) == 'list':
            # Add the reviews to the list
            redis_conn.rpush(key, *reviews)
        else:
            # Handle the case where the key exists but is not a list
            print(f"Error: Key '{key}' exists but is not of type 'list'")
    else:
        # If the key does not exist, create a new list with the reviews
        redis_conn.rpush(key, *reviews)


def get_reviews2(redis_conn, postal_code):
    key = postal_code
    # Check if the key exists and is of type 'list'
    if redis_conn.exists(key) and redis_conn.type(key) == 'list':
        reviews_data = redis_conn.lrange(key, 0, -1)
        return reviews_data if reviews_data else []
    else:
        return []



# (unchanged) print all data in the database
def print_all_data(redis_conn):
    keys = redis_conn.keys('*')
    for key in keys:
        if redis_conn.type(key) == 'list':
            print(f"{key}:")
            reviews = redis_conn.lrange(key, 0, -1)
            for idx, review in enumerate(reviews, start=1):
                print(f"  Review {idx}: {review}")
        elif redis_conn.type(key) == 'hash':
            name = redis_conn.hget(key, 'name')
            postal_code = redis_conn.hget(key, 'postal_code')
            location = redis_conn.hget(key, 'location')
            print(f"{key} - Name: {name}, Postal Code: {postal_code}, Location: {location}")

# (unchanged) clear the entire database
def clear_table(redis_conn):
    redis_conn.flushdb()
    print("Table cleared successfully.")

# (unchanged) search for a restaurant in the database
def search(redis_conn, postal_code):
    key = postal_code
    return redis_conn.exists(key)

if __name__ == "__main__":
   
    # Connect to Redis
    redis_conn = connect_to_redis()
    clear_table(redis_conn)
    '''
    # Example Usage:
    # Define reviews and postal code
    reviews_to_add = [
        str(Review("John", 4, "Great place!")),
        str(Review("Alice", 5, "Amazing food!")),
        # Add more reviews as needed
    ]
    postal_code_to_search = "12345"

    # Add reviews to the database
    add_reviews(redis_conn, postal_code_to_search, reviews_to_add)

    # Retrieve and print reviews for the specified postal code
    retrieved_reviews = get_reviews2(redis_conn, postal_code_to_search)
    print("Retrieved Reviews:")
    for idx, review in enumerate(retrieved_reviews, start=1):
        print(f"  Review {idx}: {review}")

    # Print all data in the database
    print_all_data(redis_conn)
        '''