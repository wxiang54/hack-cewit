import requests, json
from pprint import pprint

'''
if __name__ == "__main__" or __name__ == "apiUtils":
    PATH_CLIENT_SECRET = "../data/client_secret.json"
else:
'''
PATH_CLIENT_SECRET = "/var/www/ghostwallet/ghostwallet/data/client_secret.json"
    
def request_token():
    f = open(PATH_CLIENT_SECRET, 'rb').read()
    creds_json = json.loads(f)["web"]

    url = 'https://hack.softheon.io/oauth2/connect/token'
    auth = (creds_json["client_id"], creds_json["client_secret"])
    headers = {'Accept': 'application/json',
               'content-type': 'application/x-www-form-urlencoded'}
    payload = {"grant_type":"client_credentials",
               "scope":"paymentapi"}
    r = requests.post(url=url, headers=headers, auth=auth, data=payload)
    return r.json()['access_token']

'''
* CreditCardRequestModel = {
    "cardNumber": "...",
    "securityCode": "...",
    "expirationMonth": ...,
    "expirationYear": ...,
    "cardHolderName": "...",
    "billingAddress": {
        "address1": "...",
        "city": "...",
        "state": "...",
        "zipCode": "..."
    },
    "email": "...",
    "referenceId": "..."
} '''
'''
RESPONSE (one of two):
{"status": "Authorized",
 "token" : "<token>"}
OR
{"status" : "Invalid",
 "message": "<message>"}
'''
def tokenize(ccrm, access_token):
    url = 'https://hack.softheon.io/api/payments/v1/creditcards'
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + access_token}
    payload = ccrm
    r = requests.post(url=url, headers=headers, data=payload)
    r_json = r.json()
    if is_authorized(r_json):
        return {"status": "Authorized", "token": r_json.get('token')}
    return {"status": "Invalid", "message": get_response_msg(r_json)}


#helper fxn to check if CreditCardResponseModel authorized
#expect response is in parsed JSON
def is_authorized(response):
    if response.get("cardState"):
        return response["cardState"] == "Authorized"
    return "Success" in (response.get("message"), response.get("Message"))

#helper fxn to get CreditCardResponseModel (error) msg
def get_response_msg(response):
    if response.get("message"):
        return response["message"]
    if response.get("Message"):
        if response.get("ModelState"):
            #very spaghetti, change this
            return response["ModelState"][next(iter(response["ModelState"]))][0]
    #raise Exception("Can't find a message")
    return ""

#helper for fxn in dbUtils
def get_vcards_by_email_H(refID, access_token):
    url = 'https://hack.softheon.io/api/payments/v1/creditcards?referenceId={}'.format(refID)
    headers = {'Content-type': 'application/json',
               'Authorization': 'Bearer ' + access_token}
    r = requests.get(url=url, headers=headers)
    return r.json()[0]

def get_vcard_by_refID(refID):
    url = 'https://hack.softheon.io/api/payments/v1/creditcards?referenceId={}'.format(refID)
    headers = {'Content-type': 'application/json',
               'Authorization': 'Bearer ' + request_token()}
    r = requests.get(url=url, headers=headers)
    return r.json()[0]

def charge_card_by_token(token, amt):
    url = 'https://hack.softheon.io/api/payments/v1/payments'
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer ' + request_token()}
    payload = {
        "paymentAmount": amt,
        "description": "Charge for new VCard",
        #"referenceId": "example_payment",
        "paymentMethod": {
            "paymentToken": token,
            "type": "Credit Card"
        }}
    r = requests.post(url=url, headers=headers, data=payload)
    return r.json()
    

if __name__ == "__main__":
    ccrm = '''
{
    "cardNumber": "4134185779995000",
    "securityCode": "123",
    "expirationMonth": 11,
    "expirationYear": 2020,
    "cardHolderName": "John Doe",
    "billingAddress": {
        "address1": "1500 Stony Brook Road",
        "city": "Stony Brook",
        "state": "NY",
        "zipCode": "11790"
    },
    "email": "jdoe@example.com",
    "referenceId": "credit_card_example",
}'''
    print tokenize(ccrm, request_token())


