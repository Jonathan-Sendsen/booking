"""
download mongodb
create the following directories for your project
data
data/db
data/logpython

pip install pymongo


"""
from pymongo import MongoClient


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host="127.0.0.1", port=27017):
        """
        be sure to use the ip address not name for local windows
        CAUTION: Don't do this in production!!!
        """

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def print_mdb_collection(collection_name):
    for doc in collection_name.find():
        print(doc)


def main():
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media

        cd = db["cd"]

        cd_ip = {"artist": "The Who", "Title": "By Numbers"}
        cd.insert_one(cd_ip)

        cd_ip = [
            {
                "artist": "Deep Purple",
                "Title": "Made In Japan",
                "name": "Andy",
            },
            {
                "artist": "Led Zeppelin",
                "Title": "House of the Holy",
                "name": "Andy",
            },
            {"artist": "Pink Floyd", "Title": "DSOM", "name": "Andy"},
            {
                "artist": "Albert Hammond",
                "Title": "Free Electric Band",
                "name": "Sam",
            },
            {"artist": "Nilsson", "Title": "Without You", "name": "Sam"},
        ]
        cd.insert_many(cd_ip)

        print_mdb_collection(cd)

        collector = db["collector"]
        collector_ip = [
            {"name": "Andy", "preference": "Rock"},
            {"name": "Sam", "preference": "Pop"},
        ]

        collector.insert_many(collector_ip)
        print_mdb_collection(collector)

        # related data
        for name in collector.find():
            print(f'List for {name["name"]}')
            query = {"name": name["name"]}
            for a_cd in cd.find(query):
                print(f'{name["name"]} has collected {a_cd}')

        yorn = input("Drop data?")
        if yorn.upper() in ("Y", "YES"):
            cd.drop()
            collector.drop()


if __name__ == "__main__":
    main()
