
from scrapy.conf import settings
from peewee import *


db = SqliteDatabase(settings['DB'])


class BaseModel(Model):
    class Meta:
        database = db


class Logo(BaseModel):
    id = AutoField(primary_key=True)
    logo_url = CharField()
    web_url = CharField()


def create_tables():
    with db:
        db.create_tables([Logo])

