# main.py
from flask import Flask, jsonify, request
from jwks import generate_key, get_jwks
from auth import authenticate, issue_jwt

#from flask import Flask, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import jwt
#import datetime
import time

app = Flask(__name__)

# Generate a key pair
key = generate_key()



# Serve JWKS endpoint
@app.route("/.well-known/jwks.json", methods=["GET"])
def jwks():
    return jsonify(get_jwks(key))

# Authentication endpoint
@app.route('/auth', methods=['POST'])
def auth():
    expired = request.args.get('expired')
    if expired:
        jwt = issue_jwt(key, expired=True)
    else:
        jwt = issue_jwt(key)
    return jwt

if __name__ == '__main__':
    app.run(port=8080)


#jwks.py
#import time

def generate_key():
    # Generate RSA key pair
    # Associate a key ID (kid) and expiry timestamp
    return {
        'kid': 'key1',
        'rsa': {
            'n': 'public_key',
            'e': 'exponent'
        },
        'exp': int(time.time()) + 3600 # Expire in 1 hour
    }

def get_jwks(key):
    if int(time.time()) < key['exp']:
        return {
            'keys': [key]
        }
    else:
        return {
            'keys': []
        }


#auth.py
    

    # auth.py
#import jwt
#import time

def authenticate(username, password):
    # Mock authentication
    return username == 'user' and password == 'pass'

def issue_jwt(key, expired=False):
    if expired:
        key['exp'] = int(time.time()) - 3600 # Expired key
    payload = {'sub': 'user'}
    return jwt.encode(payload, key['rsa'], algorithm='RS256', headers={'kid': key['kid']})



#authEndPoint.py

#An /auth endpoint that returns an unexpired, signed JWT on a POST request
#This file is for authentifying the JWT

