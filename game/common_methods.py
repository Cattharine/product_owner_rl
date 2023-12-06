def clamp(x, minimum, maximum):
    if x < minimum:
        return minimum
    elif x > maximum:
        return maximum
    return x


def stepify(s, step):
    return (s // step) * step