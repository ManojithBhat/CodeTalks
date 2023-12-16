import os,secrets
from PIL import Image
from flask import url_for
from flask import current_app

#as the name of the profile picture could be same. we can reduce teh collision by using random hex no.
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    #it separates the file name and the extension
    #it is usual practice to use _ as variable name that won't be used latr onsend
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pic',picture_fn)

    form_picture.save(picture_path)
    #The save method is often a method provided by the FileField or FileStorage object in WTForms. This method is used to save the uploaded file to a specific location on your server.
    
    return picture_fn



