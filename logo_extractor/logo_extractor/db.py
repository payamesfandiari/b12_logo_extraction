
from scrapy.utils.project import get_project_settings
from peewee import *
from json import dumps

settings = get_project_settings()
db = SqliteDatabase(settings.get('DB','logo.db'))

class BaseModel(Model):
    class Meta:
        database = db


class Logo(BaseModel):
    """
    Scrapy extracted Item.
    """
    id = AutoField(primary_key=True)
    logo_url = CharField()
    web_url = CharField()


def create_tables():
    """
    Create the tables.
    """
    with db:
        db.create_tables([Logo])


