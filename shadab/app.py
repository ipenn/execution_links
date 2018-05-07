from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask.json import jsonify
from flask import request
from datetime import datetime
from werkzeug.exceptions import BadRequest
import client as c
import connection as conn

app, db, Order = conn.init_conn()
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/exec_links"
# db = SQLAlchemy(app)

# class Order(db.Model):
#     __tablename__ = "order"
#     #id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.String(64), primary_key=True)
#     user_id = db.Column(db.Integer)
#     product_id = db.Column(db.Text)
#     type = db.Column(db.Text)
#     side = db.Column(db.Integer)
#     ask_price = db.Column(db.Integer)
#     total_qty = db.Column(db.Integer)
#     exchange_id = db.Column(db.Text)
#     order_stamp = db.Column(db.Text)
#     OrigClOrdID = db.Column(db.Text)
#     status = db.Column(db.Text)

#     def __init__(self, order_id):
#        # self.side = side
#         #self.user_id = user_id
#         #self.product_id = product_id
#         #self.exchange_id = exchange_id
#         self.order_id = order_id
#         #self.ask_price = ask_price
#         #self.total_qty = total_quantity


# try:
client, application = c.init_test_client()
# except (fix.ConfigError, fix.RuntimeError), e:
#     print(e)


@app.route('/')
def index():
    return "Hello"

@app.route('/get', methods=['GET'])
def give():
    data = {"hey": "there"}
    return jsonify(data)


@app.route('/api/v1/new_order', methods=['POST'])
def new_order():
    print('--',request.data)
    if request.data :
        print("Request data: " + request.data)
        order_data = json.loads(request.data)
        new_ord = Order(order_data['order_id'])
        new_ord.user_id = (order_data['user_id'])
        new_ord.product_id = order_data['product_id']
        new_ord.type = "new"
        new_ord.side = (order_data['side'])
        new_ord.ask_price = (order_data['ask_price'])
        new_ord.total_qty = (order_data['total_qty'])
        new_ord.exchange_id = order_data['exchange_id']
        new_ord.order_stamp = str(datetime.utcnow())
        new_ord.status = "PendingNew"
        #new_ord.OrigClOrdID = order_data['order_id']
        db.session.add(new_ord)

#	order_data2 ={"order_id":"1","user_id":"sk96","product_id":"GOOGL","side":"0","ask_price":"80","total_qty":"30","order_stamp":"20071123-05:30:00.000","type":"1"}
        application.new_order(order_data) # written by shadab
        db.session.commit()
        res = {"success": True}
        return jsonify(res)
    else:
        res = {"success": False}
        return jsonify(res)


@app.route('/api/v1/delete_order', methods=['POST'])
def delete_order():
    print("---", request.data)
    if request.data :
        order_data = json.loads(request.data)
        new_ord = Order(order_data['order_id'])
        new_ord.user_id = (order_data['user_id'])
        new_ord.product_id = order_data['product_id']
        new_ord.OrigClOrdID = order_data['OrigClOrdID']
        new_ord.type = "delete_order"
        new_ord.order_stamp = str(datetime.utcnow())
        new_ord.status = "PendingNew"
        db.session.add(new_ord)
        # updating original order
        ##TODO
        #order = Order.query.filter_by(order_id=order_data['OrigClOrdID']).first()
        #order.status = "Cancelled"  #only when notification from ME received
        #db.session.commit

        application.cancel_order(order_data) # written by shadab
        db.session.commit()

        res = {"success": True}
        return jsonify(res)
    else:
        res = {"success": False}
        return jsonify(res)


@app.route('/api/v1/update_order', methods=['POST'])
def update_order():
    if request.data :
        order_data = json.loads(request.data)
        new_ord = Order(order_data['order_id'])
        new_ord.user_id = order_data['user_id']
        new_ord.product_id = order_data['product_id']
        new_ord.OrigClOrdID = order_data['OrigClOrdID']
        new_ord.side = order_data['side']
        new_ord.ask_price = order_data['ask_price']
        new_ord.total_qty = order_data['total_qty']
        new_ord.exchange_id = order_data['exchange_id']
        new_ord.type = "update_order"
        new_ord.order_stamp = str(datetime.utcnow())
        new_ord.status = "PendingNew"
        db.session.add(new_ord)


        application.replace_order(order_data)
        db.session.commit()

        res = {"success": True}
        return jsonify(res)
    else:
        res = {"success": False}
        return jsonify(res)


# this url will be fired by the ME to send the exec_report
@app.route('/api/v1/matching_engine', methods=['POST'])
def fill_data():
    pass
    # read data and convert to Json
    # send a post http call to OME with that json


if __name__ == "__main__":
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    app.run(host='0.0.0.0', port=8080)
