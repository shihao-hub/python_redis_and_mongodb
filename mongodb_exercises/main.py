import traceback
from pprint import pformat, pprint

import pymongo
import mongoengine
from mongoengine import Document
from mongoengine import (
    StringField, BooleanField, IntField, LongField, FloatField, DecimalField,
    ListField,
    DictField,

    MapField, SequenceField, SortedListField,
    DateField, DateTimeField, URLField, EmailField, UUIDField, FileField, EnumField, ImageField,

    PointField, BinaryField, DynamicField, PolygonField,
    ReferenceField, GeoPointField, ObjectIdField, LineStringField,
    MultiPointField, MultiPolygonField, CachedReferenceField,
    LazyReferenceField, EmbeddedDocumentField, GenericReferenceField,
    ComplexDateTimeField, MultiLineStringField, GeoJsonBaseField,
    EmbeddedDocumentListField, GenericEmbeddedDocumentField, GenericLazyReferenceField,
)


class User(Document):
    # 注意，这一个类代表一张表了！妙！
    #   但是还要注意，目前我对数据建模、数据结构的设计、SQL、MongoDB 的使用都还不行（2024-09-09）
    #   希望能够尽快牛起来！加油！
    username = StringField(required=True)
    email = StringField(required=True)
    products = ListField(required=True)


conn = pymongo.MongoClient(host="localhost", port=27017)

print(conn.list_database_names())


class CollectionManager:
    def __init__(self, db, name):
        self._db = db
        self._name = name

    def inserts(self):
        pass


def test_mail_app_db():
    db = conn.get_database("mail_app")
    print(db.collection_names())
    co = db.get_collection("drafts")

    try:
        co.insert_one({"name": "草稿1"})

        cursor = co.find()
        print(pformat(cursor.next()))
        print(pformat(cursor.next()))
        del cursor
    except StopIteration as e:
        print(e.__class__)
    finally:
        co.delete_one({"name": "草稿1"})
        print(list(co.find()))


def test():
    mongoengine.connect("mail_app")
    # 创建新用户

    user = User(username='john_doe3', email='john@example.com', products=[1, 2, 3, [123]])
    if not User.objects(username="john_doe3"):
        user.save()

    # 查询用户
    user = User.objects(username='john_doe2').first()
    print(user.email, user.products)
    print(User.objects.all())
    print(User.objects.count())
    print(type(User.objects()))
    print(type(list(User.objects())[0]))


if __name__ == '__main__':
    # test_mail_app_db()
    test()
