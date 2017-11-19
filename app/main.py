from flask import Flask
from flask_restful import Resource, Api
from models import Product, Order_fm, Customer
#from woocommerce import API
#from woocommerce1 import *

app = Flask(__name__)
api = Api(app)


#app.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
api.add_resource(Product, '/products',
                 '/products/',
                 '/products/menu',
                 '/products/<int:productID>',
                 '/products/<string:category>')


api.add_resource(Customer,'/create_customer',
                '/customers/<int:customerID>',
                '/customers')

api.add_resource(Order_fm,'/order', '/order/','/order/<int:orderID>')

#api.add_resource(Order,'/create_order')

if __name__ == '__main__':
    app.run(debug=True)
