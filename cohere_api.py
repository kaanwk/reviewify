import cohere
from cohere.responses.classify import Example
co = cohere.Client("") #ADD KEY HERE

def classify_reviews(inputs):
  examples=[
    #Positive reviews
    Example("I loved this restaurant. Nicest McDonald's location that I've been too. The store was very busy both at the drive thru and the inside. Plenty of seating inside, either downstairs or upstairs. I liked the view from the upstairs dining portion. The selection and freshness of the baked goods here was excellent. In the New York stores there isn't as much of baked good selections.", "positive"), 
    Example("Tried the new Chicken Big Mac. Really good. Maybe even better than the regular Big Mac. I got it hot off the grill, and they didn't skimp on the Special Sauce. Wish they would do a vegetarian option, though. Just replace the patties with old school veggie burgers (not those new lab-grown varieties).", "positive"),
    Example("The Mighty McMuffin!   Wow. My two favs up to now are the sausage McMuffin and the bacon McMuffin. More you can get them together. Had to get two.", "positive"), 
    Example("This is a great place. I visited when the restaurant was overwhelmed with orders with long quest of cu see Homer's to be served, but throughout, the staffs we calms friendly in attending and ensuring all customers were promptly served.", "positive"), 
    Example("I would recommend this to others", "positive"),
    #Negative reviews
    Example("Why do you accept skip orders when you are too busy to take them? 1.5 hours of waiting for your restaurant and can't even bloody confirm if you're making my food or not. Do you have no respect for customers? Reject the order when it comes in if you're so busy!", "negative"), 
    Example("manager was being beyond aggressive to one of the employees. yelling in front of the whole restaurant to “help”. when he did, she yelled at him again and then later yelled at him for not taking orders at the counter. don’t know where she thinks she works but it’s not that deep.", "negative"), 
    Example("worst mcdonalds location. Staff are beyond ridiculous after repeating myself for which drink i had wanted 4 times in a row they still gave me the wrong drink , asked for a tray to carry our food to dining area and was given a drink tray. Not to mention finding hair in our food and the dining area being absolutely filthy.", "negative"),
    Example("Not clean. Keeping the restaurant clean doesn't seem to be a priority. Washrooms are better to avoid. Order gets cleared from queue without completion for multiple customers, takes follow ups to get it and still not what was ordered. Eventually everything got fixed, but it took much longer than usual. A lot of staff seem to be lost and afraid to engage with customers. There are a few employees that seem to be pulling the workload for the rest of the team.", "negative"),
    Example("Service was super slow whenever there were 7 employees or more behind the counter. Waited over 20 minutes for 2 happy meals and only one customer has been served since. Employees don't care, they are slow. 3 over 4 of the ordering screens were not working properly, and most of the customers use them; as employees were calling order numbers while the ordering screens did not provide any receipts. The place was filthy.", "negative"),
    #Unrelated reviews
    Example("The elephants in the kitchen were a unique touch. I've never had a salad tossed by a pachyderm before, but it added to the ambiance. Five stars for creativity!", "unrelated"),
    Example("The menu was written in hieroglyphics, and I don't speak ancient Egyptian. Tried ordering the 'Pharaoh's Feast,' ended up with a pyramid of marshmallows. Confusing, but surprisingly tasty.", "unrelated"),
    Example("The chef must have mistaken my order for a treasure map because my dish arrived with an 'X' marked in chocolate syrup. Couldn't find any gold, but the dessert was golden.", "unrelated"),
    Example("I asked for a burger without pickles, but they served me a pickle sandwich without the bread. The staff insisted it was a 'deconstructed masterpiece.' I call it a cucumber catastrophe.", "unrelated"),
    Example("The waitstaff was friendly, but the chairs were actually disguised robots. One of them tried to tell me a knock-knock joke. It's a restaurant, not a comedy club. Points for unexpected entertainment.", "unrelated"),
  ]

  #Categorize reviews using cohere classify method
  response = co.classify(
    inputs=inputs,
    examples=examples,
  )

  #Append the input and classification to a 2d array to return, and count the number of positive, negative, and unrelated reviews
  positive = 0
  negative = 0
  unrelated = 0
  for i in response:
    classified_result = [[i.input, i.predictions[0]] for i in response]
    if (i.predictions[0] == 'positive'):
      positive += 1
    elif (i.predictions[0] == 'negative'):
      negative += 1
    else:
      unrelated += 1

  return classified_result, positive, negative, unrelated

def summarize_reviews(classified_reviews):
  positive_text = "Summarize the following to 2-3 sentences in an informative fashion, in third person, and with a general tone: "
  negative_text = "Summarize the following to 2-3 sentences in an informative fashion, in third person, and with a general tone: "

  #Concatenate positive and negative reviews to their respective strings
  for i in classified_reviews:
    if (i[1] == 'positive'):
      positive_text += positive_text + " " + i[0]
    elif (i[1] == 'negative'):
      negative_text += negative_text + " " + i[0]

  #Summarize reviews and present it in an informative tone using coheres chat function
  positive_response = co.chat(
	  positive_text, 
	  model="command", 
	  temperature=0.9
  )

  negative_response = co.chat(
	  negative_text, 
	  model="command", 
	  temperature=0.9
  )

  #Split the test by the '\n' character, since the last line of the chat response is irrelevant information
  positive_summary = positive_response.text.split('\n', 1)
  negative_summary = negative_response.text.split('\n', 1)

  return [positive_summary[0], negative_summary[0]]

def main():
  #Hard coded inputs for testing
  inputs=[
    "Worst experience on McDelivery. I was waiting for almost 30 minutes for a Doordash pickup along side many other delivery person. Store staff is unprofessional and do not respond to the doorbell which is specifically installed for delivery person.",
    "Sending a shout out to the manager or store person who packed in an extra McDouble for free, possibly for the long wait of my order. Whether that was intentional or not, was cool to get a freebie.",
    "The chef must have taken a detour through outer space before crafting my dish. I ordered spaghetti and got a constellation of noodles orbiting a meatball planet. A cosmic culinary experience that left my taste buds lost in space!",
    "Don't even bother going here, we've lived in this area now since February and every single time we've gotten food from here they mess up our order for forget half our food.",
    "Hot fresh food served by flight friendly staff in a very clean restaurant.  Two hamburger patties two slices of tomato pickle ketchup and mustard with a side order of small fries makes for a perfect gluten-free lunch for a Celiac like me.",
    "Seems like they played hockey with the burgers before putting in the bag. Soda machine alway messes up and gives you a nasty tasting drink. Also they keep forgetting to put sweet and sour sauce for nuggets when I not only ask for it but I always ask for extra and pay for it too...",
    "It a McDonald's! Nothing out of the expected. Ordered from the totem and grabbed it on the balcony. The place is quite nice, we sat on the second floor tables and had a great time!"
  ]

  classified_result, pos, neg, unrel = classify_reviews(inputs)

  summary = summarize_reviews(classified_result)
  print("positive summary:")
  print(summary[0])
  print("negative summary:")
  print(summary[1])

if __name__ == "__main__":
    main()

