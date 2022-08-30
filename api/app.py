# from flask import Flask, jsonify, request
# from list import shop_list
# app = Flask(__name__)

# @app.route('/shop', methods=['POST'])
# def create_shop():
#     request_data = request.get_json()
#     print(request_data)
#     print(type(request_data))
#     new_shop = {
#         'name' :  request_data['name'],
#         'items' : []
#     }
#     shop_list.append(new_shop)
#     return jsonify(new_shop)

# @app.route('/shop/<string:shop_name>', methods=['GET'])
# def get_shop_detal(shop_name):
#     for shop in shop_list:
#         if shop['name'] == shop_name:
#             return jsonify(shop)
#     return jsonify({'message' : 'shop not found'})

# @app.route('/shop', methods=['GET'])
# def get_shop_list():
#     return jsonify({'shop_list': shop_list})

# # class ShopList(Recource):
# #     def get(self):
# #         return {'shop_list' : shop_list}
    
# # api.add_resource(ShopList, '/shop')

# @app.route('/shop/<string:shop_name>/item', methods=['POST'])
# def create_item_in_shop(shop_name):
#     request_data = request.get_json()
#     for shop in shop_list:
#         if shop['name'] == shop_name:
#             new_item={
#                 'name' : request_data['name'],
#                 'price' : request_data['price']
#             }
#             shop['items'].append(new_item)
#             return jsonify(new_item)
#     return jsonify({'message' : 'shop not found'})

# # @app.route('/shop/<string:shop_name>/item', methods=['GET'])
# # def get_item_list_in_shop(shop_name):
# #     pass

# if __name__ == '__main__':
#     app.run()

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

animals = [{'name' : 'cat', 'age' : 10}]
class Animal(Resource):
    
    def get(self, name):
        for animal in animals:
            if animal['name'] == name:
                return animal
    
    def post(self, name):
        data =request.get_json()
        animal = {'name' : name, 'age' : data['age']}
        animals.append(animal)
        return animal
    
    # def put(self, name):
    #     data = request.get_json()
    #     animals.update(data)
    #     return data
    
    def delete(self, name):
        pass
    
class AnimalList(Resource):
    def get(self):
        return animals
    
api.add_resource(Animal, '/animal/<string:name>')
api.add_resource(AnimalList, '/animals')

if __name__ == "__main__":
    app.run(debug=True)