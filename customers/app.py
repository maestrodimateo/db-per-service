from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'

db = SQLAlchemy(app)

class Customer(db.Model):

    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(150), nullable = False)
    public_id = db.Column(db.String(255), unique = True, default = uuid4().hex)



@app.route('/customers', methods = ['GET'])
def get_customers():
    customers = Customer.query.all()
    all_customers = []
    for customer in customers:
        data = {}
        data['fullname'] = customer.fullname
        data['public_id'] = customer.public_id
        all_customers.append(data)

    return jsonify({'customers': all_customers})

@app.route('/customers/<string:public_id>', methods = ['GET'])
def get_customer(public_id):
    customer = Customer.query.filter_by(public_id = public_id).first()

    if not customer:
        return jsonify({'error': 'customer not found'}), 404
    data = {}
    data['fullname'] = customer.fullname
    data['public_id'] = customer.public_id

    return jsonify({'customer': data})

@app.route('/customer', methods = ['POST'])
def create_customer():
    response = request.get_json();
    customer = Customer(fullname = response['fullname'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'response': "customer added with success"}), 201

@app.route('/customers/<string:public_id>', methods = ['DELETE'])
def delete_customer(public_id):
    customer = Customer.query.filter_by(public_id = public_id).first()
    if not customer:
        return jsonify({'error': 'customer not found'}), 404
    db.session.delete(customer)
    db.session.commit()

    return jsonify({'response': "customer deleted with success."})


if __name__ == '__main__':
    app.run(debug = True, port = 4000)