from flask_restful import Api, Resource, reqparse
from cohere_api import classify_reviews, summarize_reviews
from places import main_get_total_reviews

inputs = [
    "Worst experience on McDelivery. I was waiting for almost 30 minutes for a Doordash pickup along side many other delivery person. Store staff is unprofessional and do not respond to the doorbell which is specifically installed for delivery person.",
    "Sending a shout out to the manager or store person who packed in an extra McDouble for free, possibly for the long wait of my order. Whether that was intentional or not, was cool to get a freebie.",
    "The chef must have taken a detour through outer space before crafting my dish. I ordered spaghetti and got a constellation of noodles orbiting a meatball planet. A cosmic culinary experience that left my taste buds lost in space!",
    "Don't even bother going here, we've lived in this area now since February and every single time we've gotten food from here they mess up our order for forget half our food.",
    "Hot fresh food served by flight friendly staff in a very clean restaurant.  Two hamburger patties two slices of tomato pickle ketchup and mustard with a side order of small fries makes for a perfect gluten-free lunch for a Celiac like me.",
    "Seems like they played hockey with the burgers before putting in the bag. Soda machine alway messes up and gives you a nasty tasting drink. Also they keep forgetting to put sweet and sour sauce for nuggets when I not only ask for it but I always ask for extra and pay for it too...",
    "It a McDonald's! Nothing out of the expected. Ordered from the totem and grabbed it on the balcony. The place is quite nice, we sat on the second floor tables and had a great time!"
  ]

resturant_name = "McDonalds"
postal_code = "L8P4W3"
reviews = main_get_total_reviews(restaurant_name=resturant_name, postal_code=postal_code)
reviews_result = classify_reviews(reviews)

def calcPercentages():
  totalReviews = reviews_result[-1] + reviews_result[-2] + reviews_result[-3]
  posPercent = round(reviews_result[-3]/totalReviews*100)
  negPercent = round(reviews_result[-2]/totalReviews*100)
  unrelatedPercent = round(reviews_result[-1]/totalReviews*100)
  return [posPercent, negPercent, unrelatedPercent]
calcPercentagesr = calcPercentages()

classified_result, pos, neg, unrel = classify_reviews(reviews)
summary = summarize_reviews(classified_result)

class HelloApiHandler(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'message': [calcPercentagesr[0], calcPercentagesr[1], calcPercentagesr[2], summary[0], summary[1]]
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('message', type=str)

    args = parser.parse_args()

    print(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type' and 'message')

    request_type = args['type']
    request_json = args['message']
    # ret_status, ret_msg = ReturnData(request_type, request_json)
    # currently just returning the req straight
    ret_status = request_type
    ret_msg = request_json

    if ret_msg:
      message = "Your Message Requested: {}".format(ret_msg)
    else:
      message = "No Msg"
    
    final_ret = {"status": "Success", "message": message}

    return final_ret