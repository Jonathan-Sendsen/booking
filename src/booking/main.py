import pywebio
import builtins
from loguru import logger


class NumberOutOfRange(Exception):
    pass


class InvalidCharacterAmount(Exception):
    pass


class InvalidResponseType(Exception):
    pass

class Terminal:
    @staticmethod
    def cprint(message):
        builtins.print(message)

    @staticmethod
    def cinput(message):
        return builtins.input(message)


class Web:
    @staticmethod
    def cprint(message):
        pywebio.output.put_markdown(message)

    @staticmethod
    def cinput(message):
        return pywebio.input.input(message)


def validate_customer_name(customer_name):
    if len(customer_name) < 10:
        raise InvalidCharacterAmount
    return True


def validate_package_description(package_description):
    if len(package_description) < 10:
        raise InvalidCharacterAmount
    return True


def validate_delivery_date(delivery_date):
    if len(delivery_date) < 8:
        raise InvalidCharacterAmount
    return True


def validate_weight_kgs(weight_kgs):
    if float(weight_kgs) > 10:
        raise NumberOutOfRange
    return True


def validate_volume_cubic_meters(volume_cubic_meters):
    if float(volume_cubic_meters) > 125:
        raise NumberOutOfRange
    return True


def validate_dangerous_package(dangerous_package):
    if dangerous_package.lower() in ("yes", "no"):
        return True
    else:
        raise InvalidResponseType


def validate_international_package(international_package):
    if international_package.lower() in ("yes", "no"):
        return True
    else:
        raise InvalidResponseType


def validate_urgent_package(urgent_package):
    if urgent_package.lower() in ("yes", "no"):
        return True
    else:
        raise InvalidResponseType


def shippable_by_air(weight_kgs, volume_cubic_meters, dangerous_package, urgent_package, international_package):
    if (float(weight_kgs) < 10 or float(volume_cubic_meters) < 125) and not dangerous_package \
            and urgent_package and international_package:
        return True
    return False


def shippable_by_ocean(weight_kgs, volume_cubic_meters, urgent_package, international_package):
    if (float(weight_kgs) > 7 or float(volume_cubic_meters) > 80) \
            and not urgent_package and international_package:
        return True
    return False


def shippable_by_ground(weight_kgs, volume_cubic_meters, dangerous_package, urgent_package, international_package):
    if (float(weight_kgs) > 7 or float(volume_cubic_meters) > 80) and dangerous_package \
            and not urgent_package and not international_package:
        return True
    return False


def ground_shipping_costs(urgent_package):
    if urgent_package:
        return 45
    else:
        return 25


def ocean_shipping_costs():
    ocean_shipment_cost = 30
    return ocean_shipment_cost


def air_shipping_costs(weight_kgs, volume_cubic_meters):
    air_shipment_cost_weight = weight_kgs * 10
    air_shipment_cost_volume = volume_cubic_meters * 20
    if air_shipment_cost_volume > air_shipment_cost_weight:
        return air_shipment_cost_volume
    else:
        return air_shipment_cost_weight


def define_data():
    return {
        "customer_name": {"prompt": "What is your first and last name? ",
                          "field_value": None,
                          "validator": validate_customer_name,
                          "data_error": None},
        "package_description": {"prompt": "Please describe what your package is in a few words? ",
                                "field_value": None,
                                "validator": validate_package_description,
                                "data_error": None},
        "delivery_date": {"prompt": "When do you want to deliver the package by (month/date/year)? ",
                          "field_value": None,
                          "validator": validate_delivery_date,
                          "data_error": None},
        "weight_kgs": {"prompt": "What is the weight of your package in kgs? ",
                       "field_value": None,
                       "validator": validate_weight_kgs,
                       "data_error": None},
        "volume_cubic_meters": {"prompt": "What is the calculated volume of your package in meters? ",
                                "field_value": None,
                                "validator": validate_volume_cubic_meters,
                                "data_error": None},
        "dangerous_package": {"prompt": "Is your package dangerous [Yes/No]? ",
                              "field_value": None,
                              "validator": validate_dangerous_package,
                              "data_error": None},
        "international_package": {"prompt": "Does your package need to be shipped internationally [Yes/No]? ",
                                  'field_value': None,
                                  "validator": validate_international_package,
                                  "data_error": None},
        "urgent_package": {"prompt": "Does your package need to be shipped within 3 days [Yes/No]? ",
                           "field_value": None,
                           "validator": validate_urgent_package,
                           "data_error": None},
    }


def get_user_input(data):
    for field_name, field_data in data.items():
        field_data["field_value"] = input(field_data["prompt"])
    return data


def validate_user_inputs(data):
    for field_name, field_data in data.items():
        while not field_data["validator"](field_data["field_value"]):
            try:
                field_data["field_value"] = input(field_data["error_message"])
            except ValueError as error_message:
                print(str(error_message))
    return data


def fetch_validated_data(data):
    customer_name = data["customer_name"]["field_value"]
    package_description = data["package_description"]["field_value"]
    delivery_date = data["delivery_date"]["field_value"]

    weight_kgs = data["weight_kgs"]["field_value"]
    volume_cubic_meters = data["volume_cubic_meters"]["field_value"]

    dangerous_package = True if data["dangerous_package"]["field_value"].lower() == 'yes' else False
    urgent_package = True if data["urgent_package"]["field_value"].lower() == 'yes' else False
    international_package = True if data["international_package"]["field_value"].lower() == 'yes' else False

    return customer_name, package_description, delivery_date, weight_kgs, volume_cubic_meters, dangerous_package, \
        urgent_package, international_package


io = Terminal()
print = io.cprint
input = io.cinput


def main():
    data = define_data() # initializing data variable from dict
    user_data = get_user_input(data) # getting user inputted data
    validated_data = validate_user_inputs(user_data) # getting validated user data
    customer_name, package_description, delivery_date, weight_kgs, volume_cubic_meters, dangerous_package, \
        urgent_package, international_package = fetch_validated_data(validated_data)
    air_cost = air_shipping_costs(weight_kgs, volume_cubic_meters)
    ocean_cost = ocean_shipping_costs()
    ground_cost = ground_shipping_costs(urgent_package)

    if shippable_by_air(weight_kgs, volume_cubic_meters, dangerous_package, urgent_package, international_package):
        print(f"Thanks {customer_name}, your package is set to be delivered on {delivery_date}")
        print(f"Your shipping method will be via Air, and it will cost {air_cost}")
    elif shippable_by_ocean(weight_kgs, volume_cubic_meters, urgent_package, international_package):
        print(f"Thanks {customer_name}, your package is set to be delivered on {delivery_date}")
        print(f"Your shipping method will be via Ocean, and it will cost {ocean_cost}")
    elif shippable_by_ground(weight_kgs, volume_cubic_meters, dangerous_package, urgent_package, international_package):
        print(f"Thanks {customer_name}, your package is set to be delivered on {delivery_date}")
        print(f"Your shipping method will be via Ground, and it will cost {ground_cost}")
    else:
        print("Sorry we don't ship your type of package")


if __name__ == '__main__':
    main()










