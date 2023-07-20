import random

class Person:
    class Employee:
        def __init__(self, title=None, yoe=None, position=None):
            self.title = title if title is not None else random.choice(["PM", "Marketing", "Design"])
            self.yoe = yoe if yoe is not None else random.randint(0, 15)
            self.position = position if position is not None else random.choice(["Manager", "C-level", "IC"])


# Function notes

# instance_variable initializes a class
# use a class when you are referencing a thing or make code more readable
# static method belongs to the class specifically vs the instance of the class

# when do you need function arguments?
# 1 when the function relies on objects (i.e classes)
# 2 when the function relies on external info
# 3 when the function has different conditional outputs within it (if, elif)

# when you dont need a function arguments?
# 1 when the function does the same thing without external info

# -------------------------------------------------------
# tomorrow read optimal booking code + add certain code?
# tomorrow get to rich project
# does the function adequately describe what it actually does? and is it a unique thing? If "and" in function name = too big
