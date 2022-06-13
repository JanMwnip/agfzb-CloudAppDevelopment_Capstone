import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EmotionOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
        #if api_key:
        #    # Basic authentication GET
        #    requests.get(url, params=params, headers={'Content-Type': 'application/json'},
        #                            auth=HTTPBasicAuth('apikey', api_key))
        #else:
        #    # no authentication GET
        #    response = requests.get(url, headers={'Content-Type': 'application/json'},
        #                            params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("Payload: ", json_payload, ". Params: ", kwargs)
    print(f"POST {url}")
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 json=json_payload, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["doc"]
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
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
#    json_result = get_request(url, dealerId=dealer_id)
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_reviews = json_result["result"]
        # For each dealer object
        for dealer_view_doc in dealer_reviews:
            # Get its content in `doc` object
#            dealer_view_doc = dealer_review["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_view_obj = DealerReview(dealership=dealer_view_doc["dealership"], name=dealer_view_doc["name"], purchase=dealer_view_doc["purchase"],
                                   review=dealer_view_doc["review"], purchase_date=dealer_view_doc["purchase_date"], car_make=dealer_view_doc["car_make"],
                                   car_model=dealer_view_doc["car_model"],
                                   car_year=dealer_view_doc["car_year"], sentiment=analyze_review_sentiments(url), id=dealer_view_doc["id"])#dealer_view_doc["review"]
            results.append(dealer_view_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/fcdd8f37-fac7-400b-aed9-8f2f727612cf'
    #API_KEY = os.getenv('NLU_API_KEY')
    api_key = 'pKHt8kjZqRmuxH7aDvAkKo9I6ZZLKZtyD8kR-eS08JfM'
    #params = json.dumps({"text": text, "features": {"sentiment": {}}})
    #response = requests.post(
    #    URL, data=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', API_KEY)
    #)
    params = dict()
    #params["text"] = kwargs[str(dealerreview)]
    #params["text"] = str(dealerreview)#kwargs["text"]
    #params["version"] = "2022-04-07"#kwargs["2022-04-07"]
    #params["features"] = "sentiment"#kwargs["1"]
    #params["return_analyzed_text"] = True#kwargs[True]
    #params = json.dumps({"text": str(dealerreview), "features": {"sentiment": {}}})
    #response = requests.get(URL, params=params, headers={'Content-Type': 'application/json'},
    #                                auth=HTTPBasicAuth('apikey', api_key))

    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(URL)

    response = natural_language_understanding.analyze(
        html=str(dealerreview),
        features=Features(emotion=EmotionOptions(entities=EntitiesOptions(emotion=True, sentiment=True, limit=2)))).get_result()

    try:
        #return response.json()['sentiment']['document']['label']
        #return 'Happy'
        return json.dumps(response, indent=2)
    except KeyError:
        return 'bad'#neutral


