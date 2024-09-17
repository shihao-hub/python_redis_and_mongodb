import datetime
import json
import pprint

import pymongo
import mongoengine
from mongoengine import (
    StringField, BooleanField, IntField, FloatField,
    ListField,
    DictField,
    ObjectIdField, DateField, DateTimeField,
    EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField,
    Document, DynamicDocument, ReferenceField,
)
from bson import ObjectId

DATABASE_NAME = "electronic_business"
DATABASE_HOST = "localhost"
DATABASE_PORT = 27017
DATABASE_NAME_ALIAS = DATABASE_NAME + "_alias"

# (Q)!: 如何获取当前所在地的时区？
TIME_ZONE = datetime.timezone(datetime.timedelta(hours=8))

mongoengine.connect(db=DATABASE_NAME, alias=DATABASE_NAME_ALIAS, host=DATABASE_HOST, port=DATABASE_PORT)


class Details(EmbeddedDocument):
    weight = IntField(required=True)
    weight_units = StringField(required=True)
    model_num = IntField(required=True)
    manufacturer = StringField(required=True)
    color = StringField(required=True)


class Product(Document):
    id = ObjectIdField(required=True, primary_key=True, default=ObjectId())
    slug = StringField(required=True)
    sku = StringField(required=True)
    name = StringField(required=True)
    description = StringField(required=True)
    # details = EmbeddedDocumentField(Details, required=True)
    details = DictField(required=True)
    total_reviews = IntField(required=True)
    average_review = IntField(required=True)
    created_time = DateTimeField(required=True)  # 该字段为新添加的字段，以前没有，则以前的值为 None

    meta = {
        "collection": "c_products",
        "db_alias": DATABASE_NAME_ALIAS,
    }

    objects: mongoengine.QuerySet


def test_product():
    print(datetime.datetime.now(tz=TIME_ZONE))
    doc = {
        "id": ObjectId("66e82782d238000cb2b90ecb"),  # 66e82782d238000cb2b90ecb
        "slug": "wheelbarrow-9092",
        "sku": "9092",
        "name": "Extra",
        "description": "",
        "details": json.loads(Details(**{
            "weight": 47,
            "weight_units": "lbs",
            "model_num": 111,
            "manufacturer": "Acme",
            "color": "Green",
        }).to_json()),
        "total_reviews": 411,
        "average_review": 4.5,
        "created_time": datetime.datetime.now(tz=TIME_ZONE)
    }
    print(Product.objects.filter(id=doc.get("id")).update_one(upsert=True, **doc))

    obj1: Product = Product.objects.get(id=doc.get("id"))
    obj2: Product = Product.objects.all().skip(1).limit(1).first()
    print(obj2)
    obj3 = Product.objects.filter(id=doc.get("id")).all()
    # print(obj1.to_json())
    print(obj1.created_time)
    print(obj2.created_time)

    # product_qs = Product.objects.filter(details__weight=47)
    # for obj in product_qs:
    #     pass


# for e in Product.objects.filter().all():
#     print(e)


if __name__ == '__main__':
    test_product()
    pass
