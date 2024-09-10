import collections
import json
import pprint
from collections import OrderedDict

import pymongo
from bson.objectid import ObjectId

conn = pymongo.MongoClient(host="localhost", port=27017)


# 最佳实践：在同一个集合中永远不要为同一个键保存多种类型

def test_import_json():
    db = conn.get_database("users")
    co = db.get_collection("mongodb_test_json")
    co.drop()
    data = json.load(open(r"./mongodb_test.json", "r", encoding="utf-8"))
    co.insert_one(data)
    try:
        pprint.pprint(next(co.find({
            "students.likes.username": "小红",
        })))
    except StopIteration:
        print("未查询到")


def test_users_db():
    db = conn.get_database("users")
    co = db.get_collection("user")
    co.insert_one(dict(username="张三"))

    cursor = co.find({"$where": """
    function() {
        return this._id == "66dfb8be24899e6428f5c2ba";
    }
    """})

    pprint.pprint(list(cursor))

    # def reduce(doc, aggregator):
    #     aggregator.count += 1
    #
    # print(list(co.group(*OrderedDict(
    #     key={"_id": True},
    #     condition={},
    #     initial={"count": 0},
    #     reduce=reduce
    # ).values())))


if __name__ == '__main__':
    test_users_db()
    # test_import_json()
    pass
