"""A generic DBMS independent API for CQRS"""


def save(database, data):
    database.store(data)


# queries - private
def audit_trail(database):
    return database.dump()


# query api - will use meltano to ship
def latest(database, search_key):
    current = dict()
    for record in database.dump():
        if search_key == record["payload"]["identity"]:
            for key, value in record.items():
                current.update(value)
    return current


def count_query(database, field):
    query_results = {}
    count = 0
    for record in database:
        count += 1
        dept_key = record["payload"].get(field, None)
        query_results[dept_key] = count
    return query_results


def publish(event):
    # i can notify interested subscribers when something happens
    pass


def subscribe(event):
    # receive changes from elsewhere
    pass
