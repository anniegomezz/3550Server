#Creating server using Flask

#import libraries
from flask import Flask, request, jsonify
#import datetime to deal with expiration dates
from datetime import datetime, timedelta
#import cryptography 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import jwt
#for encoding using base64
#import base64


#Create Flask application
app = Flask(__name__)

# Dictionary to store RSA keys with their expiration time
keys = {} #TO-DO - move to file as well as jwks.json, read in jwks to that

# Generates the rsa key pair (set expiration date to arbitrary time)
def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537, #same as AQAB for base64
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    #key_id = str(len(keys) + 1)
    key_id = "whyhellothere" #custom key name, change for each key that is generated
    expiration_time = datetime.utcnow() + timedelta(days=40)  # Keys are set to expire in 40 days
    keys[key_id] = (public_key, private_key, expiration_time)
    return key_id

# JWKS endpoint
#check on port 8080
@app.route("/.well-known/jwks.json", methods=["GET"]) #specifically use .well-known/jwks.json to store the jwks
def jwks(): #define the jwks function
    jwks_keys = [] #dictionary to store jwks 
    for kid, (public_key, _, expiration_time) in keys.items():
        if datetime.utcnow() < expiration_time:
            jwks_keys.append({ #append to list
                "kid": kid,
                "kty": "RSA",
                "alg": "RS256",
                #"use": "sig",
                #"n": public_key.public_numbers().n,
                #"e": public_key.public_numbers().e
                 "e": 'AQAB'
                 #TO-DO - adjust n-value
            })
    return jsonify(keys=jwks_keys)

# Authentication endpoint
@app.route('/auth', methods=['POST']) #everytime a post message is sent
def authenticate():
    expired = request.args.get('expired')
    if expired: #if the key is expired 
        key_id = list(keys.keys())[0]  # Choose the first key for expired token
    else:
        key_id = generate_rsa_key() #generates new key if old one is expired
    private_key = keys[key_id][1] #uses fir
    expiration_time = keys[key_id][2] #sets expiration time for the key
    payload = {'username': 'fakeuser', 'exp': expiration_time}
    token = jwt.encode(payload, private_key, algorithm='RS256', headers={'kid': key_id})
    return jsonify(token=token) #return token at the localhost


#App is running on port 8080 as specified in the rubric.
if __name__ == '__main__':
    app.run(port=8080)