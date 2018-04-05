import json
import yaml

with open("config.yaml", 'r') as stream:
	d = yaml.load(stream)

# load conversion dictionary
def seek(s, kv):
	with open("config.yaml", 'r') as stream:
		d = yaml.load(stream)
		if s in d[kv]:
			return d[kv][s]
		else:
			return -1

def json2fix(s):
	ret = '8=FIX.'+str(d['fix_version'])+str(d['dlm'])
	req_dict = json.loads(s)
#	print(json.dumps(req_dict, indent=4)
	for k,v in req_dict.items():
		tag = seek(k, 'tag_dict')
		value = seek(v, 'msg_dict')
		if tag == -1:
			tag = str(k)
		elif value == -1:
			value = str(v)
		ret += str(tag)+'='+str(value)+str(d['dlm'])
	return ret

st='{"OrderID":1,"MsgType":"NewOrderSingle","SenderCompID":"sk96","Symbol":"GOOGL","Side":1,"Price":80,"OrderQty":30,"SendingTime":"20071123-05:30:00.000"}'
s='{"order_id":1,"user_id":"sk96","product_id":"GOOGL","side":0,"ask_price":80,"total_qty":30,"order_stamp":"20071123-05:30:00.000","state":4,"type":1}'
res = json2fix(s)
print(res)
