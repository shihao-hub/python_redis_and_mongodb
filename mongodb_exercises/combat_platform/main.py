import contextlib
import json

import pymongo
import mongoengine
from mongoengine import (
    StringField, BooleanField, IntField, FloatField,
    ListField,
    DictField,
    Document, DynamicDocument,
)

DB_NAME = "combat_platform"


@contextlib.contextmanager
def mongoengine_connect(db_name):
    mongoengine.connect(db_name)
    yield
    mongoengine.disconnect()


class DesktopVulnerability(DynamicDocument):
    warningNo = StringField(verbose_name="问题单号", primary_key=True, required=True)
    warningName = StringField(verbose_name="")
    appCode = StringField(verbose_name="")
    appModuleName = StringField(verbose_name="")
    subProductCode = StringField(verbose_name="")
    subProductName = StringField(verbose_name="")
    productCode = StringField(verbose_name="")
    productName = StringField(verbose_name="")
    appId = StringField(verbose_name="")
    cvss = StringField(verbose_name="")
    cveId = StringField(verbose_name="")
    isBounder = BooleanField(verbose_name="")
    hwitvdId = StringField(verbose_name="")
    hwpsirtId = StringField(verbose_name="")
    warningPriority = StringField(verbose_name="")
    status = StringField(verbose_name="")
    warningSlaStatus = StringField(verbose_name="")
    confirmSlaStatus = StringField(verbose_name="")
    vulnerabilityType = StringField(verbose_name="")
    effectiveStatus = StringField(verbose_name="")
    creator = StringField(verbose_name="")
    rectificationOwner = StringField(verbose_name="")
    warningTime = StringField(verbose_name="")
    discoveryTime = StringField(verbose_name="")
    confirmTime = StringField(verbose_name="")
    closedTime = StringField(verbose_name="")
    plannedClosedTime = StringField(verbose_name="")
    lastUpdateTime = StringField(verbose_name="")
    vulnerabilityDescription = StringField(verbose_name="")
    rectificationMeasures = StringField(verbose_name="")

    meta = {
        "collection": "c_desktop_vulnerability"
    }

    objects: mongoengine.QuerySet


class VulnerabilityTrackingTask(Document):
    pass


def generate_desktop_vulnerability_collection():
    with open("./desktop_vulnerability_information.json", "r", encoding="utf-8") as file:
        data = json.load(file).get("data")
    data = data[10:20]  # 测试用
    # 注意，数据库好像连接一个就行了，集合加前缀就是咯...
    with mongoengine_connect(DB_NAME):
        docs = [DesktopVulnerability(**d) for d in data]
        DesktopVulnerability.objects.insert(docs)


if __name__ == '__main__':
    # 创建数据（一次性操作）
    # 数据库数据已经存储完毕，开始获取数据，然后利用数据。

    # 该函数设置为接口的时候就很合适了，显示是调接口的时候才会创建数据，而且显然只需要调用一次！
    # generate_desktop_vulnerability_collection()

    pass
