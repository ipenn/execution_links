from __future__ import print_function
import quickfix as fix
import time
import quickfix44 as fix44
import fix2json as f2j
import validate as val

class Application(fix.Application):
    
    orderID = 0
    mdReqID = 0

    def onCreate(self, sessionID):
        print('Application - onCreate', sessionID)
        return

    def onLogon(self, sessionID): 
        self.sessionID = sessionID
        print('Application - onLogon', sessionID)
        return

    def onLogout(self, sessionID): 
        print('Application - onLogout', sessionID)
        return

    def toAdmin(self, message, sessionID):
        print('Application - toAdmin', sessionID)
        print(message)
        return

    def toApp(self, message, sessionID): 
        print('Application - toApp', sessionID)
        return

    def fromAdmin(self, message, sessionID): 
        print('Application - fromAdmin', sessionID)
        print(message)
        return

    def fromApp(self, message, sessionID): 
        print('Application - fromApp', sessionID)
        print(message)
        # convert fix to json here
        message_str = ['|' if ord(x)==1 else x for x in message.toString()]
        message_str = ''.join(message_str)
        json_msg = f2j.fix2json(message_str)
        status, error_msg = val.validate_json(json_msg)
        if status:
            print(json_msg)
            # call OME API
            ## TODO
            print(self.get_header_value(message, fix.MsgType()))
        else:
            # raise error
            print("JSON not valid")
            print(error_msg)
        return

    def get_header_value(self, message, field): 
        key = field
        message.getHeader().getField(key)
        return key.getValue()

    def gen_orderID(self):
        self.orderID += 1
        return `self.orderID`
    
    def gen_mdReqID(self):
        self.mdReqID += 1
        return `self.mdReqID`
    
    def start_new_message(self, msg_type):
        new_message = fix.Message()
        message_fields = [
            fix.BeginString(fix.BeginString_FIX44), 
            fix.MsgType(msg_type), 
            fix.TransactTime()
        ]
        for field in message_fields:
            new_message.getHeader().setField(field)
        return new_message
   
    def new_order(self, s):
        order_message = self.start_new_message(fix.MsgType_NewOrderSingle)
        message_fields = {
            # fix.ClOrdID:self.gen_orderID(),
            # s='{"order_id":1,"user_id":"sk96","product_id":"GOOGL","side":0,"ask_price":80,
            # "total_qty":30,"order_stamp":"20071123-05:30:00.000","type":1}'
            fix.ClOrdID:str(s["order_id"]),
            fix.HandlInst:fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION,
            fix.Symbol:str(s["product_id"]),
            fix.Side:fix.Side_BUY if s["side"] == "0" else fix.Side_SELL,
            fix.OrdType:fix.OrdType_LIMIT,
            fix.OrderQty:float(s["total_qty"]),
            fix.Price:float(s["ask_price"]),
        }
	print("==================")
	print(message_fields)
        for k, v in message_fields.items():
            order_message.setField(k(v))
        print(order_message.toString())
        fix.Session.sendToTarget(order_message, self.sessionID)

    def cancel_order(self, s):
        order_message = self.start_new_message(fix.MsgType_OrderCancelRequest)
        message_fields = {
            fix.ClOrdID:str(s["order_id"]),
            fix.OrigClOrdID:str(s["OrigClOrdID"]),
            fix.Symbol:str(s["product_id"]),
            fix.Side:fix.Side_BUY if s["side"] == "0" else fix.Side_SELL,
            fix.OrderQty:float(s["total_qty"]),
        }
        for k, v in message_fields.items():
            order_message.setField(k(v))
        print(order_message.toString())
        fix.Session.sendToTarget(order_message, self.sessionID)
    
    def replace_order(self, s):
        order_message = self.start_new_message(fix.MsgType_OrderCancelReplaceRequest)
        message_fields = {
            fix.ClOrdID:str(s["order_id"]),
            fix.OrigClOrdID:str(s["OrigClOrdID"]),
            fix.HandlInst:fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION,
            fix.Symbol:str(s["product_id"]),
            fix.Side:fix.Side_BUY if s["side"] == "0" else fix.Side_SELL,
            fix.OrdType:fix.OrdType_LIMIT,
            fix.OrderQty:float(s["total_qty"]),
            fix.Price:float(s["ask_price"]),
        }
        for k, v in message_fields.items():
            order_message.setField(k(v))
        print(order_message.toString())
        fix.Session.sendToTarget(order_message, self.sessionID)

    def market_data_request(self):
        request = fix44.MarketDataRequest()
        request.setField(fix.MDReqID(self.gen_mdReqID()))
        request.setField(fix.MarketDepth(0))
        request.setField(fix.SubscriptionRequestType('0'))

        group = fix44.MarketDataRequest().NoMDEntryTypes()
        group.setField(fix.MDEntryType('0'))
        request.addGroup(group)
        group.setField(fix.MDEntryType('1'))
        request.addGroup(group)

        group = fix44.MarketDataRequest().NoRelatedSym()
        group.setField(fix.Symbol('SNAP'))
        request.addGroup(group)

        fix.Session.sendToTarget(request, self.sessionID)

def init_test_client():
    try:
        settings = fix.SessionSettings('client.cfg')
        application = Application()
        storeFactory = fix.FileStoreFactory(settings)
        logFactory = fix.FileLogFactory(settings)
        client = fix.SocketInitiator(application, storeFactory, settings, logFactory)
        client.start()
        return client, application
    except (fix.ConfigError, fix.RuntimeError), e:
        print(e)
