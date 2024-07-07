import graphene
from ...features.visitor.mantra.mantra import CreateMantraFeature

class Mutation(graphene.ObjectType):
    create_mantra_feature = CreateMantraFeature.Field()