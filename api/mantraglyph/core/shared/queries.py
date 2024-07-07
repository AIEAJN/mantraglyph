import graphene
from ..services.mantraglyph.query import MantraglyphQuery


class HelloWorldQuery(graphene.ObjectType):
    hello_world = graphene.String()

    def resolve_hello_world(root, info, **kwargs):
        return "Hello World, I'm Mantraglyph!"


class Query(MantraglyphQuery, HelloWorldQuery):
    pass
