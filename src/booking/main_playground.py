def validate_customer_name(customer_name):
    if len(customer_name) < 10:
        return False
    return True


def validate_package_description(package_description):
    if len(package_description) < 10:
        return False
    return True


def validate_weight_kgs(weight):
    if float(weight) > 10:
        return False
    return True


def validate_dangerous_package(dangerous_package):
    if dangerous_package.lower() in ("yes", "no"):
        return True
    return False


def validate_international_package(international_package):
    if international_package.lower() in ("yes", "no"):
        return True
    return False


def shippable_by_air(weight, international_package, dangerous_package):
    if 0.1 <= float(weight) <= 6.1 and international_package \
            and not dangerous_package:
        return True
    return False


def shippable_by_ground(weight, international_package, dangerous_package):
    if 6.2 <= float(weight) <= 10 and not international_package \
            and dangerous_package:
        return True
    return False


def air_cost():
    return 25


def ground_cost(weight):
    weight_cost = weight * 10
    return weight_cost


def create_data():
    return {
        "customer_name": {"prompt": "What is your name? ",
                          "field_value": None,
                          "validator": validate_customer_name},
        "package_description": {"prompt": "What is the description? ",
                                "field_value": None,
                                "validator": validate_package_description},
        "weight_kgs": {"prompt": "What is the weight of your package in kgs? ",
                       "field_value": None,
                       "validator": validate_weight_kgs},
        "international_package": {"prompt": "Is your package international? ",
                                   "field_value": None,
                                   "validator": validate_international_package},
        "dangerous_package": {"prompt": "Is your package dangerous? ",
                              "field_value": None,
                              "validator": validate_dangerous_package},
    }


def get_user_inputs(data):
    for field_name, field_data in data.items():
        field_data["field_value"] = input(field_data["prompt"])
    return data


def validate_user_inputs(user_data):
    for field_name, field_data in user_data.items():
        while not field_data["validator"](field_data["field_value"]):
            input("incorrect response try again... ")
            break
    return user_data


def fetch_user_data(validated_data):
    customer_name = validated_data["customer_name"]["field_value"]
    package_description = validated_data["package_description"]["field_value"]
    weight = validated_data["weight_kgs"]["field_value"]
    international_package = True if validated_data["international_package"]["field_value"].lower() == "yes" else False
    dangerous_package = True if validated_data["dangerous_package"]["field_value"].lower() == "yes" else False

    return customer_name, package_description, weight, international_package, \
        dangerous_package


def main():
    data = create_data()
    user_data = get_user_inputs(data)
    validated_data = validate_user_inputs(user_data)
    customer_name, package_description, weight, international_package, \
        dangerous_package = fetch_user_data(validated_data)

    if shippable_by_air(weight, international_package, dangerous_package):
        print(f'Your package will be shipped by air - {customer_name}')
        print(package_description)
        print(f'Your package will cost {air_cost()}')
    else:
        shippable_by_ground(weight, international_package, dangerous_package)
        print(f'Your package will be shipped by ground - {customer_name}')
        print(package_description)
        print(f'Your package will cost{ground_cost(weight)}')


if __name__ == "__main__":
    main()
