from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask import request
from datetime import datetime
from werkzeug.exceptions import BadRequest
import requests


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/exec_links"
db = SQLAlchemy(app)


class Order(db.Model):
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    side = db.Column(db.Boolean)
    ask_price = db.Column(db.Integer)
    total_quantity = db.Column(db.Float)
    ticker = db.Column(db.Text)
    fill_id = db.Column(db.Integer)
    quantity_done = db.Column(db.Float)
    price = db.Column(db.Integer)
    exchange_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    state = db.Column(db.Integer)

    def __init__(self, side, ask_price, total_quantity):
        self.side = side
        self.ask_price = ask_price
        self.total_quantity = total_quantity


@app.route('/')
def index():
    return "Hello"


@app.route('/api/v1/new_order', methods=['POST'])
def new_order():
    if request.data :
        order_data = json.loads(request.data)
        new_ord = Order(order_data['side'], order_data['ask_price'], order_data['total_quantity'])

        # add other attributes if reqd e.g:
        new_ord.timestamp = datetime.utcnow()
        db.session.add(new_ord)
        db.session.commit()

        send_to_ME(some_parameter)  # written by shadab

        return "Status 200 Edit successful"
    else:
        raise BadRequest()


@app.route('/api/v1/update_order/<int: id>',  methods=['DELETE', 'PUT'])
def update_order():
    if request.method == 'DELETE':
        if True:  # check condition if the request can be deleted
            order = Order.query.filter_by(order_id=id).first()
            db.session.delete(order)
            db.session.commit()
            return "Status 200 Delete successful"
        else:
            raise BadRequest()
    if request.method == 'PUT':
        if True:  # check condition if any
            order = Order.query.filter_by(order_id=id).first()
            # update order object
            db.session.commit()

            send_to_ME(some_parameter)  # written by shadab

            return "Status 200 Edit successful"
        else:
            raise BadRequest()


# this url will be fired by the ME to send the exec_report
@app.route('/api/v1/matching_engine', methods=['POST'])
def fill_data():
    # read data and convert to Json
    # send a post http call to OME with that json



if __name__ == "__main__":
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    app.run(debug=True)