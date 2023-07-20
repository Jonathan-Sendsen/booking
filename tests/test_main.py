import booking.main


def test_validate_general_information():
    customer_name = "Jonathan, Sendsen"
    package_description = "This is a test description."
    delivery_date = "October/1/2023"
    assert booking.main.validate_general_information(customer_name, package_description, delivery_date)


def test_validate_metrics():
    weight_kgs = 9.7
    volume_cubic_meters = 124
    assert booking.main.validate_metrics(weight_kgs, volume_cubic_meters)


def test_validate_package_classification():
    dangerous_package = False
    urgent_package = False
    international_package = False
    assert booking.main.validate_package_classification(dangerous_package, urgent_package, international_package)


def test_shippable_by_air():
    dangerous_package = False
    urgent_package = True
    weight_kgs = 9.7
    volume_cubic_meters = 124
    assert booking.main.shippable_by_air(weight_kgs, volume_cubic_meters, dangerous_package, urgent_package)


def test_shippable_by_ground():
    weight_kgs = 8.9
    volume_cubic_meters = 101
    urgent_package = False
    dangerous_package = True
    assert booking.main.shippable_by_ground(weight_kgs, volume_cubic_meters, urgent_package, dangerous_package)


def test_shippable_by_ocean():
    weight_kgs = 8.5
    volume_cubic_meters = 121
    urgent_package = False
    international_package = True
    assert booking.main.shippable_by_ocean(weight_kgs, volume_cubic_meters, urgent_package, international_package)


def test_get_user_inputs():
    pass


def test_ground_shipping_costs():
    assert booking.main.ground_shipping_costs(True) == 45
    assert booking.main.ground_shipping_costs(False) == 25


def test_ocean_shipping_costs():
    assert booking.main.ocean_shipping_costs() == 30


def test_air_shipping_costs():
    weight_kgs = 8
    volume_cubic_meters = 121
    air_shipment_cost_weight = weight_kgs * 10
    air_shipment_cost_volume = volume_cubic_meters * 20
    expected_cost = max(air_shipment_cost_volume, air_shipment_cost_weight)
    assert booking.main.air_shipping_costs(weight_kgs, volume_cubic_meters) == expected_cost








