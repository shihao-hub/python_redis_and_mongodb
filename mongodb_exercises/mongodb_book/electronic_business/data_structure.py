import json
import pprint
from typing import (
    List,
    Dict,
    Union, Any
)

import pydantic
import pymongo
import mongoengine
from pydantic import BaseModel, Field, Extra
from bson import ObjectId

DATABASE_NAME = "electronic_business"
DATABASE_HOST = "localhost"
DATABASE_PORT = 27017

conn = pymongo.MongoClient(host=DATABASE_HOST, port=DATABASE_PORT)
db = conn.get_database(DATABASE_NAME)


class ModuleConfigMixin:
    class Config:
        extra = Extra.allow  # 本来就是为了伸缩性，那么显然应该要设置这个吧？或者默认忽略？严格到极致就是 forbid！

    @pydantic.validator("id")
    def validate_id(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value


class Details(ModuleConfigMixin, BaseModel):
    weight: int
    weight_units: str
    model_num: int
    manufacturer: str
    color: str


class Product(ModuleConfigMixin, BaseModel):
    pk: str = Field(default=str(ObjectId()), alias="_id")
    slug: str
    sku: str
    name: str
    description: str
    details: Details = Field(default_factory=Details)
    total_reviews: int
    average_review: int

    def dict(self, *args, **kwargs):
        res = super().dict(*args, **kwargs)
        if "pk" in res:
            res["_id"] = res.pop("pk")
        return res

    @staticmethod
    def get_collection_name():
        return "c_products"


def test_product():
    c_products = db.get_collection("c_products")
    # c_products.find
    doc = Product(**{
        # "_id": str(ObjectId("66e82782d238000cb2b90ecb")),
        "slug": "wheelbarrow-9092",
        "sku": "9092",
        "name": "Extra",
        "description": "",
        "details": Details(**{
            "weight": 47,
            "weight_units": "lbs",
            "model_num": 111,
            "manufacturer": "Acme",
            "color": "Green",
        }),
        "total_reviews": 411,
        "average_review": 4.5,
    })
    c_products.update_one({"_id": doc.pk}, {"$set": doc.dict()}, upsert=True)

    inst = c_products.find_one()
    print(inst)

    # res = c_products.update_one({"$or": [
    #     dict(_id=doc.get("_id")),
    #     # dict(slug=doc.get("slug"))
    # ]}, {"$set": doc}, upsert=True)
    # print(res.upserted_id, res.modified_count, res.matched_count)


if __name__ == '__main__':
    test_product()
    pass
