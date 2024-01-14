
class Restaurant:
    def __init__(self, name, postal_code, location):
        self.name = name
        self.postal_code = postal_code
        self.location = location
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def __str__(self):
        return f"Name: {self.name}\nPostal Code: {self.postal_code}\nLocation: {self.location}"