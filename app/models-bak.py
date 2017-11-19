from woocommerce import API as WoocommerceAPI
from instance.config import app_config
from flask  import jsonify
from flask_restful import Resource

config = app_config['development']
class Products:

    wcapi = WoocommerceAPI(
            url=config.WOOCOMMERCE_URL,
            consumer_key=config.WOOCOMMERCE_KEY,
            consumer_secret=config.WOOCOMMERCE_SECRET,
            wp_api=True,
            version=config.WOOCOMMERCE_VERSION
    )
    def __init__(self):
        self.wcapi = WoocommerceAPI(
            url=config.WOOCOMMERCE_URL,
            consumer_key=config.WOOCOMMERCE_KEY,
            consumer_secret=config.WOOCOMMERCE_SECRET,
            wp_api=True,
            version=config.WOOCOMMERCE_VERSION
        )

    class ProductList(Resource):
        def get(self):
            response = jsonify(Products.wcapi.get('products?sku=flanwhole').json())
            response.status_code = 200
            return response

    class Product(Resource):
        def get(self,id):
            response = jsonify(Products.wcapi.get('products/' + str(id)).json())
            response.status_code = 200
            return response
