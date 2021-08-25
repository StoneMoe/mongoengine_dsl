def smart_bool(value) -> bool:
    if isinstance(value, str):
        value = value.lower().strip()
        return value not in ['false', 'no', '0', '']
    else:
        return bool(value)
