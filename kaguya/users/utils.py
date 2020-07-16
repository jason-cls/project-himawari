import os
from flask import current_app
from PIL import Image
from random import randint


def save_picture(form_picture):
    # Change uploaded picture to random name keep ext.
    # Also resizes the photo
    random_hex = randint(0, 9999999)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # Save the picture to path
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


    