_value_cache = {}  # Dictionary to track previous values


def value_changed(key: str, new_value) -> bool:
    """
    Returns True if the value has changed since the last check, otherwise False.

    :param key: A unique key to track this value (e.g., "elevator_manual_mode").
    :param new_value: The current value to check.
    :return: True if the value has changed from its last recorded state, False otherwise.

    @Joe needed this to quiet logging
    """
    global _value_cache

    if key not in _value_cache:
        _value_cache[key] = new_value
        return False  # Do not trigger on the first check! Just store the value

    if _value_cache[key] != new_value:
        _value_cache[key] = new_value  # Update stored value
        return True

    return False
