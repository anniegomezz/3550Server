from flask import Flask


app = Flask(__name__)


@app.route("/.well-known/jwks.json", methods=["GET"])
def getJWKS() -> tuple[str, int]:
    """
    Returns a JWKS of all JWKs on the server
    """
    # do stuff
    return stuff, 200


@app.route("/auth", methods=["POST"])
def createJWT() -> tuple[str, int]:
    """
    Create a JWK and return a corresponding JWT
    """
    # do stuff here too
    return stuff, 200




#DO NOT EDIT
if __name__ == "__main__":
    app.run(port=8080)