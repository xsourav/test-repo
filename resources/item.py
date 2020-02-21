from flask_jwt import jwt_required
from flask_restful import reqparse, Resource

from section6.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float, required=True, help="This field cannot be left blank")
    parser.add_argument('store_id',
                        type=int, required=True, help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        try:
            item.insert()
        except:
            return {"message": "An error occured inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = 'DELETE FROM items WHERE name=?'
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}, 200
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}, 200

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        # return {'items': [item.json() for item in ItemModel.query.all()]}

# connection = sqlite3.connect('data.db')
# cursor = connection.cursor()
#
# query = 'SELECT * FROM items'
# result = cursor.execute(query)
# items = []
# for row in result:
#     items.append({'name': row[0], 'price': row[1]})
#
# connection.close()
# return {'items': items}
