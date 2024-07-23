import graphene
import traceback
from graphql_relay import from_global_id

from .... import models
from ....core.shared import types as types
from ....core.services.image import image as image_service
from ....core.services.scant import tools as scant_tools_service
from ....core.shared.utils.variables import  BASE_DIR


        
# 
# *********************Create Mantra Mutation *********************
class CreateMantraFeature(graphene.Mutation):
    success: bool = graphene.Boolean()
    mantraglyph: models.Mantraglyph = graphene.Field(types.MantraglyphType)
    errors: str = graphene.String()

    class Arguments():
        uri = graphene.String(required=True)
        target_language = graphene.ID(required=True)       
        
                    
    class Meta:
        pass
        
        
    @classmethod
    def mutate(cls, root, info, **kwargs):
        font = f"{BASE_DIR}\\mantraglyph\\core\\assets\\fonts\\Wurmics_Bravo.ttf"
        image = image_service.open_image_from_url(kwargs['uri'])
        image, data = scant_tools_service.dataTesseract(image)
        word_data = scant_tools_service.wordData(data)
        bubble = scant_tools_service.bubbleNotion(word_data)   
        same_line = scant_tools_service.sameLine(word_data)
        extrem_position =  scant_tools_service.extremPosition(word_data)
        bg_position = scant_tools_service.backgroundPosition(word_data)
        translate_bubble = scant_tools_service.translateBubble(bubble, 'fr')
        sentence_to_word = scant_tools_service.sentenceToWord(translate_bubble)
        bg_color = scant_tools_service.backgroundColor(image, bg_position)
        text_color = scant_tools_service.textColor(image, bg_color)
        clear_position = scant_tools_service.clearPosition(same_line)
        coord = scant_tools_service.aBcD(extrem_position) 
        scant_tools_service.clearImage(image, clear_position , bg_color)
        scant_tools_service.applyTranslations(image, sentence_to_word, coord, font, text_color)

        return None
