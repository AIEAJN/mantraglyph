import graphene
import traceback
from graphql_relay import from_global_id
from .... import models
from ....core.shared import types as types
from ....core.services.image import image as image_service


        
# 
# *********************Create Mantra Mutation *********************
class CreateMantraFeature(graphene.Mutation):
    success: bool = graphene.Boolean()
    mantraglyph: models.Mantraglyph = graphene.Field(types.MantraglyphType)
    errors: str = graphene.String()

    class Arguments:
        uri = graphene.String(required=True)
        target_language = graphene.ID(required=True)       

                    
    class Meta:
        pass
        
        
    @classmethod
    def mutate(cls, root, info, **kwargs):
        image_service.open_image_from_url(kwargs['uri'])

        return None
