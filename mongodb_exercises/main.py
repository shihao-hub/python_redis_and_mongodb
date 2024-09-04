import traceback
from pprint import pformat, pprint

import pymongo

conn = pymongo.MongoClient(host="localhost", port=27017)

print(conn.list_database_names())


def test_mail_app_db():
    db = conn.get_database("mail_app")
    print(db.collection_names())
    co = db.get_collection("drafts")

    try:
        cursor = co.find()
        print(pformat(cursor.next()))
        print(pformat(cursor.next()))
        del cursor
    except StopIteration as e:
        print(e.__class__)


if __name__ == '__main__':
    test_mail_app_db()
