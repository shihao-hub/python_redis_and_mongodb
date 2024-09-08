import traceback
from pprint import pformat, pprint

import pymongo
import mongoengine
from mongoengine import (
    Document,
    StringField, IntField, FloatField, BooleanField,
    ListField,
    DictField
)


class User(Document):
    # 注意，这一个类代表一张表了！妙不可言，妙不可言，妙不可言！
    #   但是还要注意，目前我对数据建模、数据结构的设计、SQL、MongoDB 的使用都还不行（2024-09-09）
    #   希望能够尽快牛起来！加油！
    username = StringField(required=True)
    email = StringField(required=True)
    products = ListField(required=True)


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


def test():
    mongoengine.connect("mail_app")
    # 创建新用户
    user = User(username='john_doe', email='john@example.com', products=[1, 2, 3])
    user.save()

    # 查询用户
    user = User.objects(username='john_doe').first()
    print(user.email)


if __name__ == '__main__':
    # test_mail_app_db()
    test()
