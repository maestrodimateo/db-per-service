from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'

db = SQLAlchemy(app)

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key = True)
    label = db.Column(db.String(100), unique = True, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    customer_id = db.Column(db.String(70), unique = True)
    public_id = db.Column(db.String(255), unique = True, default = uuid4().hex)



@app.route('/products', methods = ['GET'])
def get_products():
    products = Product.query.all()
    all_products = []
    for product in products:
        data = {}
        data['label'] = product.label
        data['price'] = product.price
        data['customer_id'] = product.customer_id
        data['public_id'] = product.public_id

        all_products.append(data)

    return jsonify({'products': all_products})

@app.route('/products/<string:public_id>', methods = ['GET'])
def get_product(public_id):
    product = Product.query.filter_by(public_id = public_id).first()

    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = {}
    data['label'] = product.label
    data['price'] = product.price
    data['customer_id'] = product.customer_id
    data['public_id'] = product.public_id

    return jsonify({'product': data})

@app.route('/product', methods = ['POST'])
def create_product():
    response = request.get_json();
    produit = Product(label = response['label'], price = response['price'], customer_id = response['customer_id'])
    db.session.add(produit)
    db.session.commit()
    return jsonify({'response': "product added with success"}), 201

@app.route('/products/<string:public_id>', methods = ['DELETE'])
def delete_product(public_id):
    product = Product.query.filter_by(public_id = public_id).first()
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()

    return jsonify({'response': "Product deleted with success."})


if __name__ == '__main__':
    app.run(debug = True)