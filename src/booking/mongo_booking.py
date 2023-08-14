import booking.main
import booking.utils


application_data = booking.main.define_data()
unvalidated_data = booking.main.get_user_input(application_data)
validated_data = booking.main.validate_user_inputs(unvalidated_data)


def main():
    mongo = booking.utils.MongoDBConnection()

    with mongo:
        db = mongo.connection.shipment

        shipment = db["shipment"]
        shipment_data = {}
        for field_name, field_data in validated_data.items():
            shipment_data[field_name] = field_data["field_value"]

        shipment.insert_one(shipment_data)
        booking.utils.print_mdb_collection(shipment)


if __name__ == "__main__":
    main()
