import cv2
import requests
import numpy as np


def open_image_from_url(url: str):
    response = requests.get(url)
    img_data = response.content
    img_array = np.array(
        bytearray(img_data), dtype=np.uint8
    )  # Conversion de l'image en un tableau numpy
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Décodage de l'image
    return img
