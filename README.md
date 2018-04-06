# execution_links

## how to use client module to pass json req to quickfix server:

import client as c
client, application = c.init_test_client()

call following functions accordingly:
	* client.stop()
	* application.new_order(s)
	* application.cancel_order(s)
	* application.replace_order(s)
	* application.market_data_request()

check test_client.py for reference