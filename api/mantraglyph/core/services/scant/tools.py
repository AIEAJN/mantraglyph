import cv2
import pytesseract
#from googletrans import Translator
import numpy as np
import pandas as pd
from PIL import Image, ImageFont, ImageDraw
from math import sqrt
from operator import itemgetter
import translators as ts
import os
from google.cloud import translate
from ...shared.utils.variables import BASE_DIR, CSV_COLORS


directory = os.getcwd()

def translate_text(text="Hello, world!", project_id="meetsum-399615"):
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": "en-US",
                "target_language_code": "fr",
            }
        )

    return  response.translations[0].translated_text

def dataTesseract(image):
    image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_AREA)
    image = cv2.bilateralFilter(image, 4, 200, 200)
    data = pytesseract.image_to_data(image, output_type="dict")
    return image, data




def saveCleanImage(image, image_name=str, base=str):
    """this function take an image read with opencv and the desired name for save
    she return the path for the saved image, the cleanned image.
    don't forget the extension for the image_name: .jpg, .png...
    Example: saveCleanImage(image=image, image_name="save.jpg")
    """
    os.chdir(base)
    filename = image_name
    cv2.imwrite(filename, image)
    imagePil = base+'\\'+image_name
    return imagePil

def sentenceToWord(translations_list):
    sentence_to_word_list = []
    word_list = []
    word = ""
    for sentence in translations_list:
        for letter in sentence:
            if letter == " ":
                word_list.append(word.strip())
                word = ""
            else:
                word += letter
        word_list.append(word.strip())
        sentence_to_word_list.append(word_list)
        word = ""
        word_list = []
    return sentence_to_word_list


# Get a color name on a position
def getColorName(image, position):
    x = position[0][0]
    y = position[0][1]
    B, G, R = image[y, x]
    B = int(B)
    G = int(G)
    R = int(R)
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv(CSV_COLORS, names=index, header=None)
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G -
                                                int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if(d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname, (B, G, R)


def bubbleNotion(word_data_list):
    bubble_list = []
    bubble = ""
    for word_list in word_data_list:
        for word_data in word_list:
            bubble += word_data[0]+" "
        bubble_list.append(bubble.strip())
        bubble = ""
    return bubble_list


def wordData(data):
    count_index = 0
    word_index = 0
    word_data = []
    word_data_list = []
    block_num = 0
    X = data['left']
    Y = data['top']
    T = data['text']
    B = data['block_num']
    W = data["width"]
    H = data["height"]
    for word in T:
        word_index = count_index
        word_block = B[word_index]
        if word.strip() != "":
            if word_block == block_num:
                word_data.append((word, X[word_index], Y[word_index], W[word_index],
                                  H[word_index], B[word_index], X[word_index]+W[word_index]))
                count_index += 1
            else:
                word_data.append((T[word_index-1], X[word_index-1], Y[word_index-1], W[word_index-1],
                                  H[word_index-1], B[word_index-1], X[word_index-1]+W[word_index-1]))
                word_data_list.append(word_data)
                word_data = []
                # block_num = word_block
                count_index += 1
        else:
            if word_block == block_num:
                count_index += 1
            elif word_block > block_num:
                word_data_list.append(word_data)
                word_data = []
                block_num = word_block
                count_index += 1
            else:
                pass
    word_data_list.append(word_data)
    word_data_list = [
        words_data for words_data in word_data_list if words_data != []]
    return word_data_list


def sameLine(word_data_list):
    same_line_list = []
    same_line = []
    top = word_data_list[0][0][2]
    for x in range(len(word_data_list)):
        for word_data in word_data_list[x]:
            if word_data[2] == top:
                same_line.append(word_data)
            else:
                same_line_list.append(same_line)
                same_line = [word_data]
                top = word_data[2]
    same_line_list.append(same_line)
    return same_line_list


def clearPosition(same_line_list):
    clear_position_list = [[(same_line[0][1] - 2, same_line[0][2] - 2),
                            (same_line[-1][1] + same_line[-1]
                             [3] + 2, same_line[-1][2] + same_line[-1][4] + 2),
                            same_line[0][5]]
                           for same_line in same_line_list]
    return clear_position_list


def clearImage(image, clear_position_list, bg_color_list):
    block_num = clear_position_list[0][2]
    bg_color_indice = 0
    for clear_position in clear_position_list:
        if clear_position[2] == block_num:
            cv2.rectangle(
                image, clear_position[0], clear_position[1], bg_color_list[bg_color_indice][0][1], -1)
        else:
            bg_color_indice += 1
            cv2.rectangle(
                image, clear_position[0], clear_position[1], bg_color_list[bg_color_indice][0][1], -1)
            block_num = clear_position[2]


def backgroundPosition(word_data_list):
    background_position_list = [
        [(word_data[0][1] - 5, word_data[0][2])] for word_data in word_data_list]
    return background_position_list


def textColor(image, background_color_list):
    text_color_list = [(0, 0, 0) if background_color[0][1][2] + background_color[0][1][1] + background_color[0][1][0] >= 600
                       else (255, 255, 255)
                       for background_color in background_color_list]
    return text_color_list


def backgroundColor(image, background_position_list):
    background_color_list = []
    for background_position in background_position_list:
        background_color_list.append(
            [getColorName(image, background_position)])
    return background_color_list


def translateBubble(bubble_list,target_language):
    translations_list = [translate_text(text=bubble) for bubble in bubble_list]
    return translations_list


def translatedSentences(translations_list):
    translated_sentences_list = []
    for translations in translations_list:
        translated_sentences_list.append([translations.text])
    return translated_sentences_list


def extremPosition(word_data_list):
    extrem_positon_list = list()
    for word_data in word_data_list:
        right = word_data[0][6]
        left = word_data[0][1]
        highest_word = word_data[0]
        lowest_word = word_data[-1]
        bubble_fontheight = max(word_data, key=itemgetter(4))[4]
        for x in range(len(word_data)):
            if word_data[x][6] >= right:
                right = word_data[x][6]
                rightmost_word = word_data[x]
            if word_data[x][1] <= left:
                left = word_data[x][1]
                leftmost_word = word_data[x]
            else:
                pass
        extrem_positon_list.append(
            [leftmost_word, rightmost_word, highest_word, lowest_word, bubble_fontheight])
    return extrem_positon_list


def aBcD(extrem_position_list):
    aBcD_list = []
    for extrem_position in extrem_position_list:
        xh = extrem_position[2][1]
        yh = extrem_position[2][2] - 10

        xb = extrem_position[3][1]
        yb = extrem_position[3][2] + extrem_position[3][4] + 10

        xg = extrem_position[0][1] - 10
        yg = extrem_position[0][2]

        xd = extrem_position[1][1] + extrem_position[1][3] + 10
        yd = extrem_position[1][2]
        L = ab = sqrt((xd-xg)**2)
        l = bd = sqrt((yb-yh)**2)
        a = xg, yh
        b = xd, yh
        c = xg, yb
        d = xd, yb
        bubble_fontheight = extrem_position[4]
        aBcD_list.append([xg, yh, xd, yh, xg, yb, xd,
                          yb, L, l, bubble_fontheight])
    return aBcD_list


def applyTranslations(image, sentence_to_word_list, aBcD_list, font_path, text_color_list):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)
    count = 0
    for sentence in sentence_to_word_list:
        font_size = aBcD_list[count][10] + 3
        font = ImageFont.truetype(font_path, font_size)
        Len = len(sentence)
        x = aBcD_list[count][0]
        y = aBcD_list[count][1] + 6
        ab = aBcD_list[count][8]
        index = 0
        center = 0
        text = sentence[index]
        W = draw.textlength(text, font)
        color = (0,0,0)
        while W < ab:
            if index + 1 == Len:
                if Len == 1:
                    w = draw.textlength(text, font)
                    center = (ab-w)/2
                    draw.text((x + center, y), text, color, font=font)
                    break
                else:
                    w = draw.textlength(text, font)
                    center = (ab-w)/2
                    draw.text((x + center, y), text, color, font=font)
                    break
            else:
                next_word = ' ' + sentence[index+1]
                w = draw.textlength(text + next_word, font)
                if w <= ab:
                    text += next_word
                    index += 1
                else:
                    if index == Len-1:
                        w = draw.textlength(text, font)
                        center = (ab-w)/2
                        draw.text((x + center, y), text, color, font=font)
                        break
                    else:
                        w = draw.textlength(text, font)
                        center = (ab-w)/2
                        draw.text((x + center, y), text, color, font=font)
                        text = ""
                        y += font_size
        count += 1

    image.show()
