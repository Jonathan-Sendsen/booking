# # exception handling

def divide(numerator, denominator):
    result = numerator / denominator
    return result


# is it divide's job to just do the divide and let the caller catch the error?
# NO!

# general form...
def zzzz(x, y):
    try:
        result = x // y
        #rounds the division to a whole #
    except ZeroDivisionError:
        # handle exception
        # always need to follow up with code in except block (JS)
    else:
        # executed when no exception
        # this block is optional (depending on code needs) (JS)
    finally:
        # this block is always executed
        # regardless of exception generation.
        # yes, always executed no matter what (JS)


def divide(numerator, denominator):
    try:
        result = numerator / denominator
    except ZeroDivisionError:
        # ???n what goes here
        # There should a message here otherwise an IndentationError appears (JS)
    else:
        return result
        # this will fail if no code is added into the except block (JS)
        # this code will only succeed if the except block does not fail (JS)


class InvalidInput(ValueError):
    pass

def divide(numerator, denominator):
    try:
        result = numerator / denominator
    except ZeroDivisionError as e: # assigns e to the built-in Python error message (JS)
        raise InvalidInput from e  # translate to something more meaningful
    else:
        return result


def division(numerator, denominator):
    try:
        outcome = numerator/denominator
    except ZeroDivisionError:
        print("Cannot divide by zero")
    else:
        print("this should appear if not divided by 0")
    finally:
        print("test")
        return outcome


division(1, 0)


class InvalidAge(ValueError):
    pass


def persons_age(age):
    if age < 5:
        raise InvalidAge


try:
    persons_age(3)
except ValueError as e:
    print("Sorry, your age is invalid")
    print('error message is ', str(e))


try:
    x = int("not a number")
except ValueError as e:
    print("error message is:", str(e))


# raise used when inheriting a class - lots of value here (JS)
# when raised python stops and looks for nearest except block to handle error (JS)
# if no custom class defined python will leverage built-in errors (JS)
# raise creates a sub-class to allow for better articulation of errors (JS)