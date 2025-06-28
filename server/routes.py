from flask import request, session
from flask_restful import Resource
from server.models import User, db
from schemas import UserSchema

user_schema = UserSchema()

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if not all([username, password, password_confirmation]):
            return {"error": "Missing fields"}, 400
        if password != password_confirmation:
            return {"error": "Passwords do not match"}, 400
        if User.query.filter_by(username=username).first():
            return {"error": "Username already taken"}, 409

        user = User(username=username)
        user.password_hash = password
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return user_schema.dump(user), 201
