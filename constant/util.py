def clamp(mn, mx):
    return lambda x: sorted((mn, mx, x))[1]


def maxvelocity(velocity):
    return clamp(velocity, -velocity)


def maxproportional(v):
    return lambda *args: tuple(
        map(lambda x, v=v: x * (v / max(map(abs, args + (1,)))), args)
    )
