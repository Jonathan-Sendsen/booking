def show_numbers():
    for number in range(0, 10_000_000):
        yield number


x = show_numbers()
print(x)

print(next(x))

