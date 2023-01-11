import os
from dotenv import load_dotenv
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from datetime import date
from django.conf import settings






# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    if api_key:
        try:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            params['language']='en'
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', api_key))
            return json.loads(response.text)
        except:
            print('Network exception occured')

    else:
        json_data={}
        # print(kwargs)
        print("GET from {} ".format(url))
        try:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
            status_code = response.status_code
            json_data = json.loads(response.text)
            print("With status {} ".format(status_code))
        except:
            # If any error occurs
            print("Network exception occurred")
        
        
        return json_data


def get_dealer_by_id(url, dealer_id, **kwargs):
    results = []
    # Call get_request with a URL parameter
    # - Call get_request() with specified arguments
    
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        # - Parse JSON results into a CarDealer object list
        # For each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `doc` object
            if dealer_id==int(dealer_doc['id']):
                return CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
                
            

    return None

def get_dealer_by_state(url, state, **kwargs):
    results = []
    # Call get_request with a URL parameter
    # - Call get_request() with specified arguments
    
    json_result = get_request(url, state=state)
    if json_result:
        # - Parse JSON results into a CarDealer object list
        # For each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload,  request, **kwargs):
    # if request.user.is_authenticated:
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print('Network error occured')
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    # - Call get_request() with specified arguments
    
    json_result = get_request(url)
    if json_result:
        # - Parse JSON results into a CarDealer object list
        # For each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id, **kwargs):
    results = []

    json_result = get_request(url, dealerId=dealer_id)
    # print(json_result)
    if json_result:
        reviews = json_result['docs']
        # print(reviews)

        for review in reviews:
            print(review)
            rev_obj = DealerReview(dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                id=review['id'] 
            )
            if 'purchase_date' in review:
                rev_obj.purchase_date=review['purchase_date']
            if 'car_make' in review:
                rev_obj.car_make=review['car_make']
            if 'car_model' in review:
                rev_obj.car_model=review['car_model']
            if 'car_year' in review:
                rev_obj.car_year=review['car_year']
            
            rev_obj.sentiment = analyze_review_sentiments(rev_obj.review)
            results.append(rev_obj)
            
            # print(rev_obj)
        print(results)
    return results





# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    load_dotenv()
    print("review",dealerreview)
    apikey = "mAkpKmVOaf-MkBL-sqeak0RhypN_E0SQKpEmDXpl-3S6"
    print(apikey)
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1f0a6560-4341-4838-a6ef-e91a62a3fb8e/v1/analyze"
    json_res=get_request(url,  api_key=apikey, text=dealerreview, version="2022-04-07", features='sentiment', return_analyzed_text=True)
    print("Json sentiment",json_res)
    if bool(json_res):
        return json_res['sentiment']['document']['label']
    return ''


