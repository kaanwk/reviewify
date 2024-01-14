from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
import requests
from flask import request, redirect, url_for, jsonify
import json
from cohere_api import classify_reviews, summarize_reviews
from places import main_get_total_reviews

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

# @app.route('/result/<rest>/<post>')
# def result(rest, post):
#     what = rest
#     isthis = post
#     return {what, post}

# @app.route("/", defaults={'path':''})
# def serve(path):
#     return send_from_directory(app.static_folder,'index.html')

# @app.route('/index',methods=['POST', 'GET'])
# def plsWork():
#     if request.method == 'GET':
#         return {
#       'resultStatus': 'SUCCESS',
#       'message': ['calcPercentagesr[0], calcPercentagesr[1], calcPercentagesr[2], summary[0], summary[1]']
#       }
#     if request.method == 'POST':
#         restaurant = request.form['restaurant']
#         postal = request.form['postal']
#         return redirect(url_for('result',rest = restaurant, post = postal))
class DataProcessingHandler(Resource):
    def post(self):
        data = request.get_json()
        restaurant = data.get('restaurant', '')
        postal = data.get('postal', '')

        # Perform manipulation on input1 and input2 (replace this with your actual logic)
        reviews = main_get_total_reviews(restaurant_name=restaurant, postal_code=postal)
        reviews_result = classify_reviews(reviews)
        totalReviews = reviews_result[-1] + reviews_result[-2] + reviews_result[-3]
        posPercent = round(reviews_result[-3]/totalReviews*100)
        negPercent = round(reviews_result[-2]/totalReviews*100)
        unrelatedPercent = round(reviews_result[-1]/totalReviews*100)
        classified_result, pos, neg, unrel = classify_reviews(reviews)
        summary = summarize_reviews(classified_result)

        processed_data = [posPercent, negPercent, unrelatedPercent, summary[0], summary[1], restaurant]

        response_data = {"status": "Success", "message": processed_data}
        return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)

# api.add_resource(HelloApiHandler, '/flask/hello')
api.add_resource(DataProcessingHandler, '/flask/process_data')
