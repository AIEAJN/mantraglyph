import cv2
import requests
import numpy as np
import firebase_admin
from firebase_admin import storage
import logging
import re
text  = "/app/api/mantraglyph/core/assets/mantras/4ABDPPJ.jpg"
pattern = r"\w{7}.jpg"
result = re.search(pattern, text)
print(result.group(0).removesuffix(".jpg"))
def open_image_from_url(url: str):
    response = requests.get(url)
    img_data = response.content
    img_array = np.array(
        bytearray(img_data), dtype=np.uint8
    )  # Conversion de l'image en un tableau numpy
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Décodage de l'image


def save_image_in_firebase(image_path: str) -> str:
    bucket = storage.bucket("mantraglyph")
    pattern = r"\w{7}.jpg"
    reference = re.search(pattern, text).group(0).removesuffix(".jpg")
    # Créer une référence à l'image
    blob = bucket.blob("mantra/"+reference)
    # Uploader l'image
    blob.upload_from_filename(image_path)
    # Rendre l'image publique ou définir des permissions spécifiques
    blob.make_public()
    return blob.public_url