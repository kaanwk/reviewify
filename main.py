#Import other files
from places import main_get_total_reviews
from cohere_api import classify_reviews, summarize_reviews

#Receive input from front end (business)
#Andro----------------------------------------------------------------------
#Check if business in data base. If yes skip next step
#Search for reviews using google places API. Return array of reviews
resturant_name = "McDonalds"
postal_code = "L8P4W3"
reviews = main_get_total_reviews(restaurant_name=resturant_name, postal_code=postal_code)
print("RETURNN")
print(len(reviews))
#Andro----------------------------------------------------------------------
#Send array of reviews to cohere API to classify
classified_result, pos, neg, unrel = classify_reviews(reviews)
for i in classified_result:
    print(i)
#Send classified reviews for summary
summary = summarize_reviews(classified_result)
for j in summary:
    print(j)
#Ammar----------------------------------------------------------------------
#Send classified array of feedback to front end to display
