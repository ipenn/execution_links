from fix2json import config_dict

def validate_json(json_msg):
    """
    validate a json object
    :param fix_msg: a fix message
    :return: 0 (invalid) or 1 (valoid)
    """
    json_obj = json.loads(json_msg)
    valid = True
    msg = "pass"

    # test product_id (should be in all caps)
    if not json_obj["product_id"].isupper():
        valid, msg = False, "All not caps"

    # test ask_price (should not be negative)
    elif json_obj["ask_price"] < 0:
        valid, msg = False, "ask price is negative"

     # test total_qty (should not be negative)
    elif json_obj["total_qty"] <= 0:
        valid, msg = False, "total quantity is <= 0"

    # test type (should be 1, 2, 3, or 4)
    elif json_obj["type"] not in (1, 2, 3, 4):
        valid, msg = False, "type invalid"

    # test side (should be 0 or 1)
    elif json_obj["side"] not in (0, 1):
        valid, msg = False, "side invalid"

    return valid, msg

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
                valid, msg = False, "All not caps"
                break

        # test ask_price (should not be negative)
        if entity[0] == '44':
            if float(entity[1]) < 0:
                valid, msg = False, "ask price is negative"
                break

        # test total_qty (should not be negative)
        if entity[0] == '38':
            if float(entity[1]) <= 0:
                valid, msg = False, "total quantity is <= 0"
                break

        # test type (should be 1, 2, 3, or 4)
        if entity[0] == '35':
            if entity[1] not in ('1', '2', '3', '4'):
                valid, msg = False, "type invalid"
                break

        # test side (should be 0 or 1)
        if entity[0] == '54':
            if entity[1] not in ('0', '1'):
                valid, msg = False, "side invalid"
                break

    return valid, msg
