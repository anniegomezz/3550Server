# main.py
from flask import Flask, jsonify, request
from jwks import generate_key, get_jwks
from auth import authenticate, issue_jwt

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
