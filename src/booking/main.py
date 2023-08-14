import pywebio
import builtins
from loguru import logger


class InvalidName(Exception):
    pass


class InvalidPackageDescription(Exception):
    pass


class InvalidDeliveryDate(Exception):
    pass


class NumberOutOfRange(Exception):
    pass


class InvalidResponseDangerousPackage(Exception):
    pass


class InvalidResponseUrgentPackage(Exception):
    pass


class InvalidResponseInternationalPackage(Exception):
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
        raise InvalidName
    return True, None


def validate_package_description(package_description):
    if len(package_description) < 10:
        raise InvalidPackageDescription
    return True, None


def validate_delivery_date(delivery_date):
    if len(delivery_date) < 8:
        raise InvalidDeliveryDate
    return True, None


def validate_weight_kgs(weight_kgs):
    if float(weight_kgs) > 10:
        raise NumberOutOfRange
    return True, None


def validate_volume_cubic_meters(volume_cubic_meters):
    if float(volume_cubic_meters) > 125:
        raise NumberOutOfRange
    return True, None


def validate_dangerous_package(dangerous_package):
    if dangerous_package.lower() in ("yes", "no"):
        return True, None
    else:
        raise InvalidResponseDangerousPackage


def validate_international_package(international_package):
    if international_package.lower() in ("yes", "no"):
        return True, None
    else:
        raise InvalidResponseInternationalPackage


def validate_urgent_package(urgent_package):
    if urgent_package.lower() in ("yes", "no"):
        return True, None
    else:
        raise InvalidResponseUrgentPackage


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
    weight_kgs = float(weight_kgs)
    volume_cubic_meters = float(volume_cubic_meters)
    air_shipment_cost_weight = round(weight_kgs * 10, 2)
    air_shipment_cost_volume = round(volume_cubic_meters * 20, 2)
    if air_shipment_cost_volume > air_shipment_cost_weight:
        return air_shipment_cost_volume
    else:
        return air_shipment_cost_weight


def define_data():
    return {
        "customer_name": {"prompt": "What is your first and last name? ",
                          "field_value": None,
                          "is_valid": False,
                          "validator": validate_customer_name,
                          "data_error": None},
        "package_description": {"prompt": "Please describe what your package is in a few words? ",
                                "field_value": None,
                                "is_valid": False,
                                "validator": validate_package_description,
                                "data_error": None},
        "delivery_date": {"prompt": "When do you want to deliver the package by (year/month/day)? ",
                          "field_value": None,
                          "is_valid": False,
                          "validator": validate_delivery_date,
                          "data_error": None},
        "weight_kgs": {"prompt": "What is the weight of your package in kgs? ",
                       "field_value": None,
                       "is_valid": False,
                       "validator": validate_weight_kgs,
                       "data_error": None},
        "volume_cubic_meters": {"prompt": "What is the calculated volume of your package in meters? ",
                                "field_value": None,
                                "is_valid": False,
                                "validator": validate_volume_cubic_meters,
                                "data_error": None},
        "dangerous_package": {"prompt": "Is your package dangerous [Yes/No]? ",
                              "field_value": None,
                              "is_valid": False,
                              "validator": validate_dangerous_package,
                              "data_error": None},
        "international_package": {"prompt": "Does your package need to be shipped internationally [Yes/No]? ",
                                  'field_value': None,
                                  "is_valid": False,
                                  "validator": validate_international_package,
                                  "data_error": None},
        "urgent_package": {"prompt": "Does your package need to be shipped within 3 days [Yes/No]? ",
                           "field_value": None,
                           "is_valid": False,
                           "validator": validate_urgent_package,
                           "data_error": None},
    }


def get_user_input(data):
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
            field_data["is_valid"], field_data["data_error"] = field_data["validator"](field_data["field_value"])
        except InvalidName:
            field_data["is_valid"] = False
            field_data["data_error"] = "Customer name must be > 10 characters"
        except InvalidPackageDescription:
            field_data["is_valid"] = False
            field_data["data_error"] = "Package description must be > 10 characters"
        except InvalidDeliveryDate:
            field_data["is_valid"] = False
            field_data["data_error"] = "Delivery date must be in yyyy/mm/dd format"
        except NumberOutOfRange:
            field_data["is_valid"] = False
            field_data["data_error"] = "Weight must be < 10kg and volume < 125 cubic meters"
        except InvalidResponseDangerousPackage:
            field_data["is_valid"] = False
            field_data["data_error"] = "yes or No are valid responses for dangerous packages"
        except InvalidResponseInternationalPackage:
            field_data["is_valid"] = False
            field_data["data_error"] = "yes or no are valid responses for international packages"
        except InvalidResponseUrgentPackage:
            field_data["is_valid"] = False
            field_data["data_error"] = "yes or no are valid responses for urgent packages"
        finally:
            data[field_name] = field_data
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
        data = define_data()
        while not all(field_data[1]["is_valid"] for field_data in data.items()):
            user_data = get_user_input(data)
            validated_data = validate_user_inputs(user_data)

        customer_name, package_description, delivery_date, weight_kgs,\
        volume_cubic_meters, dangerous_package, urgent_package,\
        international_package = fetch_validated_data(validated_data)
        air_cost = air_shipping_costs(weight_kgs, volume_cubic_meters)
        ocean_cost = ocean_shipping_costs()
        ground_cost = ground_shipping_costs(urgent_package)

        if customer_name and shippable_by_air(weight_kgs, volume_cubic_meters, dangerous_package,
                                              urgent_package, international_package):
            print(f"Thanks {customer_name}, your package is set to be delivered on {delivery_date}")
            print(f"Your shipping method will be via Air, and it will cost ${air_cost}")
        elif customer_name and shippable_by_ocean(weight_kgs, volume_cubic_meters, urgent_package, international_package):
            print(f"Thanks {customer_name}, your package is set to be delivered on {delivery_date}")
            print(f"Your shipping method will be via Ocean, and it will cost ${ocean_cost}")
        elif customer_name and shippable_by_ground(weight_kgs, volume_cubic_meters, dangerous_package, urgent_package,
                                                   international_package):
            print(f"Thanks {customer_name}, your package is set to be delivered on {delivery_date}")
            print(f"Your shipping method will be via Ground, and it will cost ${ground_cost}")
        else:
            print("Sorry we don't ship your type of package")


if __name__ == '__main__':
    main()























