import io
import urllib.request

import numpy as np
from PIL import Image, ImageOps
from fastapi import FastAPI, Depends, File
from fastapi import HTTPException
from keras.models import load_model
from sqlalchemy.orm import Session

import database
from user import User

app = FastAPI()


@app.post("/login")
async def login(db: Session = Depends(database.get_db), sign: bytes = File(...)):
    users = db.query(User).all()
    id = 0
    max = 0.0
    image = Image.open(io.BytesIO(sign))
    image = ImageOps.fit(image, (300, 200), Image.ANTIALIAS)

    for user in users:
        print(user.nickname)
        urllib.request.urlretrieve(user.image_url, "sample.jpg")

        background_image = Image.open("sample.jpg")

        new_image = Image.new("RGB", (600, 600), (256, 256, 256))
        new_image.paste(background_image, (0, 0, 600, 600))
        new_image.paste(image, (300, 400, 600, 600))
        new_image.save("sample.jpg")

        c_image = Image.open("sample.jpg")

        model = load_model('keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        size = (224, 224)
        c_image = ImageOps.fit(c_image, size, Image.ANTIALIAS)

        image_array = np.asarray(c_image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        if max < prediction[0][0]:
            id = user.id
            max = prediction[0][0]

    if max <= 0.3:
        print(max)
        raise HTTPException(status_code=404, detail="Not Found Sign")
    return {"id": id}
