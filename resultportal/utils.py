def safe_int(value, default=0):
    """Safely convert a value to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Safely convert a value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_str(value, default=''):
    """Safely convert a value to string"""
    if value is None:
        return default
    return str(value)