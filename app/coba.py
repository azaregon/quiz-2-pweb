def a(func):
    print("a")
    b = func()

    return b


@a
def c():
    print("ll")


c()