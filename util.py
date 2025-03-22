import math

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


# function that clamps between mn and mx
def clamp(mn, mx):
    return lambda x: sorted((mn, mx, x))[1]


# clamp between velocity and -velocity
def maxvelocity(velocity):
    return clamp(velocity, -velocity)


# limits `y` to be at most `difference` from `x`
def maxdistance(difference):
    return lambda x, y: clamp(x + difference, x - difference)(y)


# scale *args so all of *args is between v and -v
def maxproportional(v):
    return lambda *args: tuple(
        map(lambda x, v=v: x * (v / max(map(abs, args + (1,)))), args)
    )


def deadzone(zone):
    return lambda x: 0 if abs(x) < zone else x


# squares positive and negative numbers
def squaredampen(x):
    return x * x * (x // abs(x)) if x else x
