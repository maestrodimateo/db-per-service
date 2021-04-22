from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

customer_base_uri = 'http://127.0.0.1:4000/'
product_base_uri = 'http://127.0.0.1:5000/'

@app.route('/customers', methods = ['GET'])
def get_customers():
    customers = requests.get(customer_base_uri + 'customers')
    return customers.json()

@app.route('/products/customers/<string:public_id>')
def get_products_customer(public_id):
    products = requests.get(product_base_uri + 'products/customer/' + public_id)
    return products.json()

if __name__ == '__main__':
    app.run(debug = True, port = 6000)