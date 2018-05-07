from fix2json import config_dict
import json

def validate_json(json_msg):
    """
    validate a json object
    :param json_msg: a fix message
    :return: 0 (invalid) or 1 (valid)
    """
    # json_msg = json.loads(json_msg)
    valid = True
    msg = ""

    # test product_id (should be in all caps)
    if not json_msg["product_id"].isupper():
        valid = False
        msg += "All not caps; "

    # test ask_price (should not be negative)
    if json_msg["ask_price"] < 0:
        valid = False
        msg += "ask price is negative; "

     # test total_qty (should not be negative)
    if json_msg["total_qty"] <= 0:
        valid = False
        msg += "total quantity is <= 0; "

    # test type (should be 1, 2, 3, or 4)
    if json_msg["type"] not in (8, 9):
        valid = False
        msg += "type invalid; "

    # test side (should be 0 or 1)
    if json_msg["side"] not in (1, 2):
        valid = False
        msg += "side invalid; "

    if msg:
        return valid, msg
    return valid, "pass"

def validate_fix(fix_msg):
    """
    validate a fix msg
    :param fix_msg: a fix message
    :return: 0 (invalid) or 1 (valid)
    """
    fix_msg = fix_msg.split(config_dict['dlm'])

    valid = True
    msg = "pass"

    for entity in fix_msg[1:-1]: # fix_msg[1:-1] ignores the 8=FIX and the empty string at the end of fix_msg
        entity = entity.split("=")

        # test product_id (should be in all caps)
        if entity[0] == '55':
            if not entity[1].isupper():
                valid = False
                msg += "All not caps; "

        # test ask_price (should not be negative)
        if entity[0] == '44':
            if float(entity[1]) < 0:
                valid = False
                msg += "ask price is negative; "

        # test total_qty (should not be negative)
        if entity[0] == '38':
            if float(entity[1]) <= 0:
                valid = False
                msg += "total quantity is <= 0; "

        # test type (should be 1, 2, 3, or 4)
        if entity[0] == '35':
            if entity[1] not in ('1', '2', '3', '4'):
                valid = False
                msg = "type invalid; "

        # test side (should be 0 or 1)
        if entity[0] == '54':
            if entity[1] not in ('0', '1'):
                valid = False
                msg = "side invalid; "

    if msg:
        return valid, msg
    return valid, "pass"

#print validate_json('{"order_id":1,"user_id":"sk96","product_id":"GoOGL","side":3,"ask_price":-80,"total_qty":0,"order_stamp":"20071123-05:30:00.000","type":5}')