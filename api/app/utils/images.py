from PIL import Image
from io import BytesIO
from uuid import uuid4
import os
from fastapi import UploadFile

async def save_image(img : UploadFile, dest : str):
    if not os.path.exists(dest):
        os.makedirs(dest)
    file = Image.open(BytesIO(await img.read()))
    name = str(uuid4()) + '.webp'
    file.save(os.path.join(dest, name), format='WEBP')
    return name

async def remove_image(img, dest):
    path = os.path.join(dest, img)
    os.remove(path)
