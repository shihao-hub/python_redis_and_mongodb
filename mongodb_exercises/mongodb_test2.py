import json
import pprint
import time

import pymongo
import mongoengine as engine

TODAY = time.strftime("%Y-%m-%d", time.localtime())

conn = pymongo.MongoClient(host="localhost", port=27017)

db = conn.get_database("combat_platform")

with open("./mongodb_test2.json", "r", encoding="utf-8") as file:
    file_data = json.load(file)

co = db.get_collection(TODAY)
co.drop()
co.insert_one(file_data)

engine.connect("combat_platform")


class Review(engine.Document):  # EmbeddedDocument
    user = engine.StringField(required=True)
    comment = engine.StringField(required=True)
    rating = engine.IntField(required=True)
    date = engine.DateField(required=True)

    meta = dict(collection="co_review")


class Ratings(engine.Document):  # EmbeddedDocument
    average = engine.FloatField(required=True)
    reviews = engine.ListField(engine.ReferenceField(Review))  # EmbeddedDocumentField

    meta = dict(collection="co_ratings")

    def __init__(self, *args, **values):
        if "reviews" in values:
            data = values.pop("reviews")
            res = []
            for d in data:
                inst = Review(**d)
                inst.save()
                res.append(inst)
            values["reviews"] = res
        super().__init__(*args, **values)


class Product(engine.Document):
    id = engine.StringField(primary_key=True, required=True)
    title = engine.StringField(required=True)
    author = engine.StringField(required=True)
    genres = engine.ListField(engine.StringField(), required=True)
    price = engine.FloatField(required=True)
    inStock = engine.BooleanField(required=True)
    ratings = engine.ReferenceField(Ratings, required=True)  # EmbeddedDocumentField

    meta = dict(collection="co_product")

    def __init__(self, *args, **values):
        if "ratings" in values:
            data = values.pop("ratings")
            inst = Ratings(**data)
            inst.save()
            values["ratings"] = inst
        super().__init__(*args, **values)


Product.drop_collection()
Ratings.drop_collection()
Review.drop_collection()

# print("products:\n")
products = co.find_one({}, {"store.products": 1}).get("store").get("products")
for e in products:
    product = Product(**e)
    # print(pprint.pformat(e), flush=True)
    product.save()

pprint.pprint(list(db["co_ratings"].find({
    "_id": db["co_product"].find_one({}, {"ratings": 1}).get("ratings")
})))
