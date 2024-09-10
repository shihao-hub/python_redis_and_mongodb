import time

import pymongo
import mongoengine as m

conn = pymongo.MongoClient(host="localhost", port=27017)


# SLAP
# 获取接口数据
# 将接口返回的数据存入 json，可以尝试分片
# 利用 mongodb json 导入功能，将 json 导入并存入 Mongodb 数据库
# 通过 Mongodb 查询我所需要的数据

class CombatPlatformModel:
    pass


test_data = {
    "data": {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "end": True,
                        "users": [
                            {
                                "id": 1,
                                "name": "Alice",
                                "age": 30,
                                "email": "alice@example.com",
                                "address": {
                                    "street": "123 Main St",
                                    "city": "Wonderland",
                                    "zip": "12345"
                                }
                            },
                            {
                                "id": 2,
                                "name": "Bob",
                                "age": 25,
                                "email": "bob@example.com",
                                "address": {
                                    "street": "456 High St",
                                    "city": "Wonderland",
                                    "zip": "12345"
                                }
                            }
                        ]
                    }
                }
            }
        }
    }
}


def take_today_as_key():
    return time.strftime("%Y%m%d", time.localtime())


db = conn.get_database("combat_platform")
co_skeleton = db.get_collection(take_today_as_key() + ":" + "skeleton")
co_level4_users = db.get_collection(take_today_as_key() + ":" + "level4_users")
co_skeleton.drop()
co_level4_users.drop()
print("集合 :skeleton 和 :level4_users 清理完成")

skeleton = test_data.get("data")
level4 = skeleton.get("level1").get("level2").get("level3").get("level4")
level4_users = level4.pop("users")
co_level4_users.insert_many(level4_users)
level4["users"] = [e.get("_id") for e in co_level4_users.find()]
co_skeleton.insert_one(skeleton)

