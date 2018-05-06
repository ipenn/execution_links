import yaml

def invert_dict(mapping):
	"""
	inverts mapping (keys:values becomes values:keys)
	note: values are unique
	:param mapping: a dictionary
	:return:
	"""
	inv = {}
	for key, val in mapping.iteritems():
		if isinstance(val, dict):
			for k, v in val.iteritems():
				inv[str(v)] = k
		else:
			inv[str(val)] = key
	return inv
	#return {val:key for key, val in mapping.iteritems()} # dict.iteritems() is more efficient than dict.items()

with open("config.yaml") as stream:
	config_dict = yaml.load(stream)

assert isinstance(config_dict, dict)
inv_config_dict = invert_dict(config_dict)

# print inv_config_dict


def fix2json(fix_msg):
	"""
	converts a fix message to a json object
	:param fix_msg: fix message
	:return: JSON object equivalent to `fix_msg`
	"""

	equi_json = {}
	fix_msg = fix_msg.split(config_dict['dlm'])
	#print fix_msg
	for entity in fix_msg[1:-1]: # fix_msg[1:-1] ignores the 8=FIX and the empty string at the end of fix_msg
		entity = entity.split("=")
		try:
			equi_json[inv_config_dict[entity[0]]] = int(float(entity[1]))
		except ValueError:
			equi_json[inv_config_dict[entity[0]]] = entity[1]

	#print equi_json
	return str(equi_json)



#print fix2json("8=FIX.4.4|49=sk96|55=GOOGL|37=1|44=80|52=20071123-05:30:00.000|38=30|35=1|54=0|")