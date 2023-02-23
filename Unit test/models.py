from mongoengine import Document, StringField, IntField, ListField
from typing import Union

class Employee(Document):
    name: str
    age: Union[str,None] = None
    teams: Union[list,None] = None
