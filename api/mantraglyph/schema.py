import graphene
from .core.shared.queries import Query
from .core.shared.mutations import Mutation


schema = graphene.Schema(query=Query, mutation=Mutation)
