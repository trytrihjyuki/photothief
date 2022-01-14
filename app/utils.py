import json

from PIL import Image

def get_configs():
    with open('config.json', 'r') as configs_f:
        configs = json.load(configs_f)
    return configs

def set_configs(configs):
    with open('config.json', 'r+') as configs_f:
        configs_f.seek(0)
        json.dump(configs, configs_f, indent=4)
        configs_f.truncate()


def open_imgs(watermark_ext, photo_ext):
    watermark_pil = Image.open('static/uploads/watermark.' + watermark_ext)
    photo_pil = Image.open('static/uploads/photo.' + photo_ext)
    return watermark_pil, photo_pil

def resize_img():
    with open('config.json', 'r+') as configs_f:
        configs = json.load(configs_f)
        max_dim = configs['max_dim']
        watermark_ext = configs['watermark_ext']
        photo_ext = configs['photo_ext']

    # check compatibility of uploaded images
    watermark_pil, photo_pil = open_imgs(watermark_ext, photo_ext)
    watermark_size = watermark_pil.size
    photo_size = photo_pil.size
    if photo_size != watermark_size:
        raise ValueError
    
    # resize imgs to fit in max_dim parameter
    watermark_pil.thumbnail((max_dim, max_dim), Image.ANTIALIAS)
    photo_pil.thumbnail((max_dim, max_dim), Image.ANTIALIAS)
    watermark_pil.save('static/uploads/watermark.' + watermark_ext, watermark_ext.upper())
    photo_pil.save('static/uploads/photo.' + photo_ext, photo_ext.upper())

