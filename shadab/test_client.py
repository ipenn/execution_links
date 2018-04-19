from __future__ import print_function
import client as c

def main():
	try:
		client, application = c.init_test_client()
		while True:
				cmd = raw_input()
				if cmd == 'x':
					client.stop()
					break
				if cmd == 'nb':
					# new order
					s={"order_id":"1","user_id":"sk96","product_id":"GOOGL","side":"0","ask_price":"80","total_qty":"30","order_stamp":"20071123-05:30:00.000","type":"1"}
					application.new_order(s)
				if cmd == 'ns':
					# new order
					s={"order_id":"2","user_id":"sk96","product_id":"GOOGL","side":"1","ask_price":"80","total_qty":"30","order_stamp":"20071123-05:30:00.000","type":"1"}
					application.new_order(s)
				if cmd == 'c':
					# cancel order
					s={"order_id":"2","user_id":"sk96","product_id":"GOOGL","side":"0","ask_price":"80","total_qty":"30","order_stamp":"20071123-05:30:00.000","type":"4", "OrigClOrdID": "1"}
					application.cancel_order(s)
				if cmd == 'r':
					# replace order
					s={"order_id":"3","user_id":"sk96","product_id":"GOOGL","side":"0","ask_price":"80","total_qty":"40","order_stamp":"20071123-05:30:00.000","type":"2", "OrigClOrdID": "1"}
					application.replace_order(s)
				if cmd == 'm':
					# market data request
					application.market_data_request()
	except (fix.ConfigError, fix.RuntimeError), e:
		print(e)

if __name__ == '__main__':
    main()