from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
from woocommerce import API as WoocommerceAPI

# local import
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    api = Api(app, prefix="/api/v1")

    wcapi = WoocommerceAPI(
        url=app.config.get('WOOCOMMERCE_URL'),
        consumer_key = app.config.get('WOOCOMMERCE_KEY'),
        consumer_secret= app.config.get('WOOCOMMERCE_SECRET'),
        wp_api=True,
        version=app.config.get('WOOCOMMERCE_VERSION')
    )

    #@app.route('/', methods=['GET'])
    class helloworld(Resource):
        def get(self):
           response = jsonify({'hello':'world'})
           #response.status_code = 200
           return response

    @app.route('/test', methods=['GET'])
    def test():
        print(wcapi.get("products").json())
        response = jsonify(wcapi.get('products').json())
        response.status_code = 200
        return response

    @app.route('/test/<int:id>', methods=['GET'])
    def test1(id):
        print(wcapi.get("products/" +  str(id)))
        response = jsonify(wcapi.get('products/' + str(id) ).json())
        response.status_code = 200
        return response

    @app.route('/test/sku/<string:sku>', methods=['GET'])
    def test2(sku):
        print(wcapi.get("products/sku/" +  sku))
        response = jsonify(wcapi.get('products/sku/' + sku ).json())
        response.status_code = 200
        return response

    @app.route('/products/<int:id>', methods=['GET'])
    class ProductItem(Resource):
        def get(self,id):
           return "hello"

    #api.add_resource(helloworld,'/')
    #api.add_resource(Products.ProductList,'/products')
    #api.add_resource(Products.Product,'/products/<int:id>')

    return app

