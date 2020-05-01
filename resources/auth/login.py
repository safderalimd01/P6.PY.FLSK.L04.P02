from flask import Flask, request, jsonify
from flask_restful import Resource

import os

from resources.utility.config import mysql
from werkzeug.security import safe_str_cmp

from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity, fresh_jwt_required)



class ClsLogin(Resource):

    def post(self, *args, **kwargs):
        _json = request.json
        _username = _json.get('username', None)
        _password = _json.get('password', None)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT id, username, password FROM user")
            db_users = cursor.fetchall()

            username_table = {u.get('username', None): u for u in db_users}
            userid_table = {u.get('id', None): u for u in db_users}

            user = username_table.get(_username, None)
            if user and safe_str_cmp(user.get('password'), _password):
                access_token = create_access_token(identity=user.get('username'), fresh=True)
                refresh_token = create_refresh_token(identity=user.get('username'))  
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200

            return {"message": "Invalid Credentials!"}, 401
        except Exception as e:
            return {"message": str(e)}, 400
