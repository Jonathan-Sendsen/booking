# import random
#
# class Person:
#     class Employee:
#         def __init__(self, title=None, yoe=None, position=None):
#             self.title = title if title is not None else random.choice(["PM", "Marketing", "Design"])
#             self.yoe = yoe if yoe is not None else random.randint(0, 15)
#             self.position = position if position is not None else random.choice(["Manager", "C-level", "IC"])
#
#
# # Function notes
#
# # instance_variable initializes a class
# # use a class when you are referencing a thing or make code more readable
# # static method belongs to the class specifically vs the instance of the class
#
# # when do you need function arguments?
# # 1 when the function relies on objects (i.e classes)
# # 2 when the function relies on external info
# # 3 when the function has different conditional outputs within it (if, elif)
#
# # when you dont need a function arguments?
# # 1 when the function does the same thing without external info
#
# # -------------------------------------------------------
# # tomorrow read optimal booking code + add certain code?
# # tomorrow get to rich project
# # does the function adequately describe what it actually does? and is it a unique thing? If "and" in function name = too big


class InvalidName(Exception):
    pass


class InvalidPackageType(Exception):
    pass


class InvalidWeightRange(Exception):
    pass


def customer_name(customer_name):
    if len(customer_name) < 10:
        return InvalidName
    return True, None


def international_package(international_package):
    if international_package in ("yes", "no"):
        return True, None
    return InvalidPackageType


def weight_kgs(weight):
    if float(weight) > 10:
        return InvalidWeightRange
    return True, None


def shippable_by_air(international_package, weight):
    if international_package and float(weight) < 10:
        return True
    return False


def air_cost(weight):
    package_cost = float(weight * 10)
    return round(package_cost, 2)


def define_data():
    return {
        "customer_name": {"prompt": "What is your full name? ",
                          "field_value": None,
                          "is_valid": False,
                          "data_error": None,
                          "validator": customer_name},
        "international_package": {"prompt": "Is the package international [Yes/No]? ",
                                  "field_value": None,
                                  "is_valid": False,
                                  "data_error": None,
                                  "validator": international_package},
        "weight": {"prompt": "What is your weight in kgs? ",
                   "field_value": None,
                   "is_valid": False,
                   "data_error": None,
                   "validator": weight_kgs},
        }


def get_user_inputs(data):
    for field_name, field_data in data.items():
        if not field_data["is_valid"]:
            if field_data["data_error"] is not None:
                print(f"Please correct the following error => {field_data['data_error']}")
                field_data["field_value"] = input(field_data["prompt"])
        data[field_name] = field_data
    return data


def validate_user_inputs(data):
    for field_name, field_data in data.items():
        try:
            field_data["data_error"], field_data["is_valid"] = \
                field_data["validator"](field_data["field_value"])
        except InvalidName:
            field_data["is_valid"] = False
            field_data["data_error"] = "Your name must be greater than 10 characters"
        except InvalidPackageType:
            field_data["is_valid"] = False
            field_data["data_error"] = "Response is only yes or no"
        except InvalidWeightRange:
            field_data["is_valid"] = False
            field_data["data_error"] = "Package weight < 10 kgs only"
        finally:
            data[field_name] = field_data
    return data


def fetch_inputs(data):
    customer_name = data["customer_name"]["field_value"]
    international_package = True if data["international_package"]["field_value"].lower() else False
    weight_kgs = data["weight"]["field_value"]
    return customer_name, international_package, weight_kgs


def main():
    data = define_data()
    for field_name, field_data in data.items():
        while not all(field_data["is_valid"]):
            user_data = get_user_inputs(data)
            validated_data = validate_user_inputs(user_data)

    customer_name, international_package, weight_kgs = \
        fetch_inputs(validated_data)
    shipping_cost = air_cost(weight_kgs)
    if shippable_by_air(international_package):
        print(f"Your package will be shipped by air and cost ${shipping_cost}")
        print(f"Than you {customer_name}")
    else:
        print("Sorry we don't ship that package")


if __name__ == 'main':
    main()


# tomorrow write in another way?
# review rich code?
# read dev docs