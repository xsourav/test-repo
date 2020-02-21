# import os
# import sys
#
# sys.path.append(os.path.abspath(os.path.join('..', 'app')))
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from section6.resources.user import UserRegister
from section6.resources.item import Item, ItemList
from section6.security_file import authenticate, identify
from section6.resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "sourav"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identify)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from section6.db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
