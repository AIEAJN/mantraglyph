import graphene
import traceback
from graphql_relay import from_global_id
import logging
from .... import models
from ....core.shared import types as types
from ....core.services.image import image as image_service
from ....core.services.scant import tools as scant_tools_service
from ....core.shared.utils.variables import WURMIC_BRAVO
import hashlib

        
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
        logging.warning("ici0")
        
        logging.warning("ici1")
        image = image_service.open_image_from_url(kwargs['uri'])
        logging.warning("ici2")
        image, data = scant_tools_service.dataTesseract(image)
        logging.warning("ici3")
        word_data = scant_tools_service.wordData(data)
        logging.warning("ici4")
        bubble = scant_tools_service.bubbleNotion(word_data)  
        logging.warning("ici5") 
        same_line = scant_tools_service.sameLine(word_data)
        logging.warning("ici6")
        extrem_position =  scant_tools_service.extremPosition(word_data)
        logging.warning("ici7")
        bg_position = scant_tools_service.backgroundPosition(word_data)
        logging.warning("ici8")
        translate_bubble = scant_tools_service.translateBubble(bubble, 'fr')
        logging.warning("ici9")
        sentence_to_word = scant_tools_service.sentenceToWord(translate_bubble)
        logging.warning("ici10")
        bg_color = scant_tools_service.backgroundColor(image, bg_position)
        logging.warning("ici11")
        text_color = scant_tools_service.textColor(image, bg_color)
        logging.warning("ici12")
        clear_position = scant_tools_service.clearPosition(same_line)
        logging.warning("ici13")
        coord = scant_tools_service.aBcD(extrem_position) 
        logging.warning("ici14")
        scant_tools_service.clearImage(image, clear_position , bg_color)
        logging.warning("ici15")
        # logging.warning(sentence_to_word, translate_bubble)
        mantra = scant_tools_service.applyTranslations(image, sentence_to_word, coord, WURMIC_BRAVO, text_color)
        hash = hashlib.sha256("mantra")
        print(
            hash
        )
        mantra.save(hash)
        logging.warning("ici16")
        return None
