from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask.json import jsonify
from flask import request
from datetime import datetime
from werkzeug.exceptions import BadRequest

def init_conn():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/exec_links"
    db = SQLAlchemy(app)

    class Order(db.Model):
        __tablename__ = "order"
        #id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.String(64), primary_key=True)
        user_id = db.Column(db.Integer)
        product_id = db.Column(db.Text)
        type = db.Column(db.Text)
        side = db.Column(db.Integer)
        ask_price = db.Column(db.Integer)
        total_qty = db.Column(db.Integer)
        exchange_id = db.Column(db.Text)
        order_stamp = db.Column(db.Text)
        OrigClOrdID = db.Column(db.Text)
        status = db.Column(db.Text)

        def __init__(self, order_id):
           # self.side = side
            #self.user_id = user_id
            #self.product_id = product_id
            #self.exchange_id = exchange_id
            self.order_id = order_id
            #self.ask_price = ask_price
            #self.total_qty = total_quantity
    return app, db, Order