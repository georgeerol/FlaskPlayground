from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
api = Api(app)
app.secret_key = 'george'
items = []

jwt = JWT(app, authenticate, identity)  # /auth


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # if name found and it's not None
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        # 1. check it's json
        # 2. needs to have content-type
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        # list of items to not be deleted
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/student/Rolf
api.add_resource(ItemList, '/items')

app.run(port=5000)
