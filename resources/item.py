from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = "this field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help = "Every item needs to have a store id"
    )

    @jwt_required()
    def get(self,name):
        row = ItemModel.find_by_name(name)
        if row:
            return row.json()
        return {'msg': 'Item not found!'}, 404    

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'msg':'An item with name "{}" already exists'.format(name)}, 400
        
        data = Item.parser.parse_args()

        item= ItemModel(name,**data)
        try:
            item.save_to_db()
        except:
            return {'msg': 'an error occurred while inserting'}, 500  #internal server error
        return item.json(), 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'msg': 'Item deleted!'}

    def put(self,name):
        data = Item.parser.parse_args()
        # row = result.fetchone()
        item = ItemModel.find_by_name(name)
        if item is None: 
            item = ItemModel(name, **data)
        else:
            item.price = data['price'] 
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}

