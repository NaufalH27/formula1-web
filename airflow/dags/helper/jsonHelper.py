def get_value(json_obj, *keys):
    try:
        value = json_obj
        for key in keys:
            value = value[key]
        return value
    
    except (KeyError, TypeError,IndexError):
        return None