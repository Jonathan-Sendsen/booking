# import numbers
from contextlib import contextmanager

FILENAME = "app.txt"


class MissingValue(Exception):
    pass


class MissingRule(Exception):
    pass


class StringInNumericField(Exception):
    pass


class ReferencDataInvalid(Exception):
    pass


class NumberOutOfRange(Exception):
    pass


class InvalidStringLength(Exception):
    pass


class InvalidDate(Exception):
    pass

# generator(remembers where it was but builds off of last state)
@contextmanager
def writable_file(file_path):
    file = open(file_path, mode="a")
    try:
        yield file
    finally:
        file.close()


@contextmanager
def readable_file(file_path):
    file = open(file_path, mode="r")
    try:
        yield file
    finally:
        file.close()


def validate(data=None, rules=None):
    if not data:
        raise MissingValue
    if not rules:
        raise MissingRule

    if rules["type"] == "reference":
        if data in rules["valid_values"]:
            return True
        raise ReferencDataInvalid

    if rules["type"] == "date":
        date_item = data.split("-")
        # only rudimentary for now
        if (
            len(data.split("-")) == 3
            and len(date_item[0].zfill(4)) == 4
            and len(date_item[1].zfill(2)) == 2
            and len(date_item[2].zfill(2)) == 2
        ):
            return True
        raise InvalidDate

    if rules["type"] == "string":
        valid = (
            rules["valid_values"][0] <= len(data) <= rules["valid_values"][1]
        )
        if valid:
            return True
        raise InvalidStringLength

    if rules["type"] == "numeric_range":
        try:
            data = float(data)
        except ValueError:
            raise StringInNumericField
        else:
            valid = (
                rules["valid_values"][0] <= data <= rules["valid_values"][1]
            )
            if valid:
                return True
            raise NumberOutOfRange
    return False

# why does "numeric_range" use try + except but "string" doesnt?
# both are essentially doing the same thing?? len vs float..


def setup():
    return {
        "booking_type": {
            "prompt": "Enter booking type: ",
            "is_valid": False,
            "value": None,
            "field_data_error": None,
            "rules": {
                "type": "reference",
                "valid_values": ("Air", "Ocean", "Truck"),
            },
        },
        "booking_description": {
            "prompt": "Enter description of booking: ",
            "is_valid": False,
            "value": None,
            "field_data_error": None,
            "rules": {"type": "string", "valid_values": (10, 40)},
        },
        "requested_delivery_date": {
            "prompt": "Enter requested delivery date: ",
            "is_valid": False,
            "value": None,
            "field_data_error": None,
            "rules": {"type": "date", "valid_values": "yyyy-mm-dd"},
        },
        "shipment_quantity": {
            "prompt": "Enter quantity of goods to ship: ",
            "is_valid": False,
            "value": None,
            "field_data_error": None,
            "rules": {"type": "numeric_range", "valid_values": (1, 100)},
        },
        "weight": {
            "prompt": "Enter weight of goods to ship: ",
            "is_valid": False,
            "value": None,
            "field_data_error": None,
            "rules": {"type": "numeric_range", "valid_values": (0.1, 20.0)},
        },
        "volume": {
            "prompt": "Enter volume of goods to ship: ",
            "is_valid": False,
            "value": None,
            "field_data_error": None,
            "rules": {"type": "numeric_range", "valid_values": (0.1, 30.0)},
        },
    }

# why not hardcode an error message vs creating a key for data_error?


def get_input(application):
    for field_name, field_data in application.items():
        if field_data["is_valid"]:
            continue
        if field_data["field_data_error"] is not None:
            print(
                f"{field_data['field_data_error']} => {field_data['value']}. Rule: {', '.join(map(str, field_data['rules']['valid_values']))}"
            )
        field_data["value"] = input(field_data["prompt"])
        application[field_name] = field_data
    return application


def validate_data(application):
    all_valid = True
    for field_name, field_data in application.items():
        try:
            if not field_data["is_valid"]:
                field_data["is_valid"] = validate(
                    field_data["value"], field_data["rules"]
                )
            else:
                continue
        except StringInNumericField:
            field_data["field_data_error"] = "Must enter a numeric value"
        except NumberOutOfRange:
            field_data["field_data_error"] = "Number out of range"
        except ReferencDataInvalid:
            field_data["field_data_error"] = "Invalid reference data value"
        except InvalidStringLength:
            field_data[
                "field_data_error"
            ] = "Invalid length: must be within parameters"
        except InvalidDate:
            field_data["field_data_error"] = "Date is not yyyy-mm-dd"
        except MissingValue:
            field_data["field_data_error"] = "Must enter data"
        except MissingRule:
            field_data["field_data_error"] = "System error: rule missing"
        finally:
            if not field_data["is_valid"]:
                all_valid = False
            else:
                field_data["field_data_error"] = None
        application[field_name] = field_data
    return application, all_valid


def save(application):
    record = {
        field_name: field_value["value"]
        for field_name, field_value in application.items()
    }
    with writable_file(FILENAME) as file:
        file.write(str(record))


def load():
    with readable_file(FILENAME) as file:
        line = file.read()
        return line


def format_data(application):
    for field_name, field_data in application.items():
        if field_data["rules"]["type"] in ("numeric_range", "number"):
            if (
                float(field_data["value"]) - int(float(field_data["value"]))
                == 0
            ):
                field_data["value"] = int(field_data["value"])
            else:
                field_data["value"] = float(field_data["value"])
        application[field_name] = field_data
    return application

# why do all functions take application? vs. passing differ args?


def main():
    application = setup()
    while True:
        unvalidated = get_input(application)
        validated, all_valid = validate_data(unvalidated)
        if all_valid:
            formatted = format_data(validated)
            break
    save(formatted)
    print(load())


if __name__ == "__main__":
    main()
