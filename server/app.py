#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(
        bakeries,
        200,
        {"Content-Type": "application/json"}
    )
    return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter_by(id=id).first()
    bakery_dict=bakery.to_dict()
    response=make_response(
        bakery_dict,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods = [baked_g.to_dict() for baked_g in baked]

    response = make_response(
        baked_goods,
        200,
        {"Content-Type": "application/json"}
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive = baked.to_dict()

    response = make_response(
        most_expensive,
        200,
        {"Content-Type": "application/json"}
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
