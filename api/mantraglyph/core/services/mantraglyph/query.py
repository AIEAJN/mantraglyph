import graphene
from . import type as type
from .... import models as models
from query_optimizer import DjangoConnectionField


class MantraglyphQuery(graphene.ObjectType):
    mantraglyph = DjangoConnectionField(type.MantraglyphType)
