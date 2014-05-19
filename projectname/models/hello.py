from schematics.models import Model
from schematics.types import StringType


class HelloWorld(Model):
    hello = StringType(required=True, choices=["world"])
