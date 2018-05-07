import fix2json as f2j
with open("testFIX.txt") as f:
	msgs = f.readlines()
	content = [x.strip() for x in msgs] 
	# print(content)
	for message in content:
		message_str = ['|' if ord(x)==1 else x for x in message]
		message_str = ''.join(message_str)
		json_msg = f2j.fix2json(message_str)
		print(json_msg)