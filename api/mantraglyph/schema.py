import graphene


class HelloWorldQuery(graphene.ObjectType):
    hello_world = graphene.String()

    def resolve_hello_world(root, info, **kwargs):
        return "Hello World, I'm Mantraglyph!"


class Query(HelloWorldQuery, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
