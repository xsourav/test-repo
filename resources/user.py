import sqlite3
from flask_restful import Resource, reqparse

from section6.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="this field cannot be empty"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cannot be empty"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
             return {"message": "Username exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successful"}, 201

    # def post(self):
    #     data = UserRegister.parser.parse_args()
    #
    #     if UserModel.find_by_username(data['username']):
    #         return {"message": "Username exists"}, 400
    #
    #     connection = sqlite3.connect('data.db')
    #
    #     cursor = connection.cursor()
    #
    #     query = "INSERT INTO users VALUES (NULL,?,?)"
    #
    #     cursor.execute(query, (data['username'], data['password']))
    #
    #     connection.commit()
    #     connection.close()
    #
    #     return {"message": "User created successful"}, 201
