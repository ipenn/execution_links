from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask import request
from datetime import datetime
from werkzeug.exceptions import BadRequest
import requests
import client as c



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/exec_links"
db = SQLAlchemy(app)

try:
    client, application = c.init_test_client()
except (fix.ConfigError, fix.RuntimeError), e:
    print(e)


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Text)
    user_id = db.Column(db.Text)
    product_id = db.Column(db.Text)
    type = db.Column(db.Text)
    side = db.Column(db.Text)
    ask_price = db.Column(db.Text)
    total_qty = db.Column(db.Text)
    ticker = db.Column(db.Text)
    fill_id = db.Column(db.Text)
    quantity_done = db.Column(db.Text)
    price = db.Column(db.Text)
    exchange_id = db.Column(db.Text)
    order_stamp = db.Column(db.Text)
    state = db.Column(db.Text)

    def __init__(self, order_id, side, ask_price, total_quantity):
        self.side = side
        self.order_id = order_id
        self.ask_price = ask_price
        self.total_qty = total_quantity


@app.route('/')
def index():
    return "Hello"


@app.route('/api/v1/new_order', methods=['POST'])
def new_order():
    if request.data :
        order_data = json.loads(request.data)
        new_ord = Order(order_data['order_id'], order_data['side'], order_data['ask_price'], order_data['total_qty'])
        # add other attributes if reqd e.g:
        new_ord.user_id = order_data['user_id']
        new_ord.product_id = order_data['product_id']
        new_ord.order_stamp = str(datetime.utcnow())
        db.session.add(new_ord)
        db.session.commit()
#	order_data2 ={"order_id":"1","user_id":"sk96","product_id":"GOOGL","side":"0","ask_price":"80","total_qty":"30","order_stamp":"20071123-05:30:00.000","type":"1"}
        application.new_order(order_data) # written by shadab

        return "Status 200 New Order added successfully"
    else:
        raise BadRequest()


@app.route('/api/v1/delete_order', methods=['POST'])
def delete_order():
    if request.data :
        order_data = json.loads(request.data)
        # add other attributes if reqd e.g:
        order = Order.query.filter_by(order_id=order_data['OrigClOrdID']).first()
        db.session.delete(order)
        db.session.commit()

        application.cancel_order(order_data) # written by shadab

        return "Status 200 Delete successful"
    else:
        raise BadRequest()


@app.route('/api/v1/update_order', methods=['POST'])
def update_order():
    if request.data :
        order_data = json.loads(request.data)
        order = Order.query.filter_by(order_id=order_data['OrigClOrdID']).first()
        order.ask_price = order_data['ask_price']
        order.total_qty = order_data['total_qty']

        db.session.commit()

        application.replace_order(order_data)
        return "Status 200 Update successful"
    else:
        raise BadRequest()


# this url will be fired by the ME to send the exec_report
@app.route('/api/v1/matching_engine', methods=['POST'])
def fill_data():
	pass
    # read data and convert to Json
    # send a post http call to OME with that json


if __name__ == "__main__":
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    app.run(host='0.0.0.0', port=8080)
