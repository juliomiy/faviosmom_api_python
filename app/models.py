from flask_restful import Resource, request
from flask import jsonify, Response
#from woocommerce import API as WoocommerceAPI
import re
import json
import sys
from faviosmom_wc import Faviosmom_wc

class BaseWooCommerce(Resource):
    response_dict = {"status_code": None,
                     "count": 0,
                     "response": [],
                     "message": None
                     }
    faviosmom_wc = Faviosmom_wc()
    return_fields = []

    def filter_return_fields(self, woocommerce_records, return_fields, default=None):
        if not return_fields:
            return woocommerce_records
        api_response_list = []
        for item in woocommerce_records:
           api_response_list.append(self.sub_dict(item,return_fields))

        return api_response_list

    def sub_dict(self, somedict, somekeys, default=None):
        return dict([(k, somedict.get(k, default)) for k in somekeys])

class Product(BaseWooCommerce):
    return_fields = ['id','name','slug','description','short_description','sku','price','regular_price','sale_price','categories']

    def get(self,productID=None,category=None):
        if re.search('\/menu$',str(request.url_rule)):
            category = "catering"

        uri = 'products'
        if productID:
            uri += '/' +  str( productID )

        try:
            wc_response =  (self.faviosmom_wc.wcapi.get(uri))
            wc_response_records = wc_response.json()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.response_dict["message"] = "Error in try/catch"
            self.response_dict["status_code"] = 500
        finally:
            if wc_response and wc_response.status_code != 200:
               self.response_dict["status_code"] = wc_response.status_code
               self.response_dict["message"] = wc_response.text
               return self.response_dict

        self.response_dict["status_code"] = wc_response.status_code

        if wc_response.status_code != 200 :
            return self.response_dict

        if category:
            product_category = []
            for item in wc_response_records:
                for cat in item['categories']:
                   if cat['slug'] == category:
                      product_category.append(item)

            wc_response_records = product_category

        if type(wc_response_records) is dict:
            t = []
            t.append(wc_response_records)
            wc_response_records = t

        api_response_list = self.filter_return_fields(wc_response_records,self.return_fields)
        self.response_dict["response"] = api_response_list
        self.response_dict["count"] = self.response_dict["response"].__len__()

        return self.response_dict


class Order_fm(BaseWooCommerce):

    def get(self,orderID=None):
        uri = 'orders'
        if orderID:
            uri += '/' +  str( orderID )
        try:
            wc_response =  (self.faviosmom_wc.wcapi.get(uri))
            wc_response_records = wc_response.json()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.response_dict["message"] = "Error in try/catch"
            self.response_dict["status_code"] = 500
        finally:
            if  wc_response.status_code != 200:
               self.response_dict["status_code"] = wc_response.status_code
               self.response_dict["message"] = wc_response_records["message"]
               return self.response_dict

        if type(wc_response_records) is dict:
            t = []
            t.append(wc_response_records)
            wc_response_records = t

        api_response_list = self.filter_return_fields(wc_response_records, self.return_fields)
        self.response_dict["response"] = api_response_list
        self.response_dict["count"] = self.response_dict["response"].__len__()
        self.response_dict["status_code"] = 200

        return self.response_dict

    def post(self):
        data = {
            "payment_method": "bacs",
            "payment_method_title": "Direct Bank Transfer",
            "set_paid": True,
            "billing": {
                "first_name": "John",
                "last_name": "Doe",
                "address_1": "969 Market",
                "address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "postcode": "94103",
                "country": "US",
                "email": "john.doe@example.com",
                "phone": "(555) 555-5555"
            },
            "shipping": {
                "first_name": "John",
                "last_name": "Doe",
                "address_1": "969 Market",
                "address_2": "",
                "city": "San Francisco",
                "state": "CA",
                "postcode": "94103",
                "country": "US"
            },
            "line_items": [
                {
                    "product_id": 93,
                    "quantity": 2
                },
                {
                    "product_id": 22,
                    "variation_id": 23,
                    "quantity": 1
                }
            ],
            "shipping_lines": [
                {
                    "method_id": "flat_rate",
                    "method_title": "Flat Rate",
                    "total": 10
                }
            ]
        }
        response = Faviosmom_wc.wcapi.post("orders", data).json()
        return response

class Customer(BaseWooCommerce):
    # get a customer record given a numeric Customer ID
    return_fields = ['id','billing','email','first_name','last_name','username']
    def get(self,customerID=None):
        uri = 'customers'
        if customerID:
            uri += '/' +  str( customerID )

        try:
            wc_response =  (self.faviosmom_wc.wcapi.get(uri))
            wc_response_records = wc_response.json()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            self.response_dict["message"] = "Error in try/catch"
            self.response_dict["status_code"] = 500
        finally:
            if wc_response and wc_response.status_code != 200:
               self.response_dict["status_code"] = wc_response.status_code
               self.response_dict["message"] = wc_response.text
               return self.response_dict
        #filter for return fields
        api_response_list = self.filter_return_fields(wc_response_records,self.return_fields)

        self.response_dict["response"] = api_response_list
        self.response_dict["count"] = self.response_dict["response"].__len__()

        self.response_dict["status_code"] = wc_response.status_code
        return self.response_dict

    def post(self):
        data = {
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "username": "john.doe",
                "password":"Yankees5a",
                "billing": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "company": "",
                    "address_1": "969 Market",
                    "address_2": "",
                    "city": "San Francisco",
                    "state": "CA",
                    "postcode": "94103",
                    "country": "US",
                    "email": "john.doe@example.com",
                    "phone": "(555) 555-5555"
                },
                "shipping": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "company": "",
                    "address_1": "969 Market",
                    "address_2": "",
                    "city": "San Francisco",
                    "state": "CA",
                    "postcode": "94103",
                    "country": "US"
                }
        }
        response = Faviosmom_wc.wcapi.post("customers", data).json()
        return response
