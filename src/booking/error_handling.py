

def divide_numbers(numerator, denominator):
    try:
        results = numerator/denominator
    except ZeroDivisionError:
        return results


try:
    print(divide_numbers(1, 0))
except ZeroDivisionError:
    raise




