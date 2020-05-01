from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
import pymysql
import os

from flask_jwt_extended import JWTManager

from resources.utility.config import app, api

from resources.auth.auth_routes import initialize_auth_routes
from resources.product.product_routes import initialize_product_routes
from resources.client.client_routes import initialize_client_routes

app.secret_key = "v3ry_s3cr3t_k3y"

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(self):
    return jsonify(
        {
            "description": "Token has expired!",
            "error": "token_expired"
        }, 401
    )


@jwt.invalid_token_loader
def invalid_token_callback(self):
    return jsonify(
        {
            "description": "Signature verification failed!",
            "error": "invalid_token"
        }, 401
    )


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify(
        {
            "description": "Access token not found!",
            "error": "unauthorized_loader"
        }, 401
    )


@jwt.needs_fresh_token_loader
def fresh_token_loader_callback(self):
    return jsonify(
        {
            "description": "Token is not fresh. Fresh token needed!",
            "error": "needs_fresh_token"
        }, 401
    )

# Route
initialize_auth_routes(api)
initialize_product_routes(api)
initialize_client_routes(api)

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=False)
