def r(seed=[0], m=2**32, a=1664525, c=1013904223):
    """
    m: modulus
    a: multiplier
    c: increment

    """

    seed[0] = (a*seed[0] + c) % m
    return seed[0]
                


if __name__ == "__main__":
    for x in range(10):
        print(r())
