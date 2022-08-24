from flask import Flask, jsonify, request
from list import shop_list
app = Flask(__name__)
@app.route('/shop', methods=['POST'])
def create_shop():
    request_data = request.get_json()
    print(request_data)
    print(type(request_data))
    new_shop = {
        'name' :  request_data['name'],
        'items' : []
    }
    shop_list.append(new_shop)
    return jsonify(new_shop)

@app.route('/shop/<string:shop_name>', methods=['GET'])
def get_shop_detal(shop_name):
    for shop in shop_list:
        if shop['name'] == shop_name:
            return jsonify(shop)
    return jsonify({'message' : 'shop not found'})

@app.route('/shop', methods=['GET'])
def get_shop_list():
    return jsonify({'shop_list': shop_list})

@app.route('/shop/<string:shop_name>/item', methods=['POST'])
def create_item_in_shop(shop_name):
    request_data = request.get_json()
    for shop in shop_list:
        if shop['name'] == shop_name:
            new_item={
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            shop['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message' : 'shop not found'})

# @app.route('/shop/<string:shop_name>/item', methods=['GET'])
# def get_item_list_in_shop(shop_name):
#     pass

if __name__ == '__main__':
    app.run()