import json

from PIL import Image, ImageDraw

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def check_file(file):
    if file and '.' in file.filename:
        extension = file.filename.split('.')[-1]
        if extension in ALLOWED_EXTENSIONS:
            return extension
    return None

def get_configs():
    with open('config.json', 'r') as configs_f:
        configs = json.load(configs_f)
    return configs

def set_configs(configs):
    with open('config.json', 'r+') as configs_f:
        configs_f.seek(0)
        json.dump(configs, configs_f, indent=4)
        configs_f.truncate()

def get_run_info():
    with open('run_info.json', 'r') as run_info_f:
        run_info = json.load(run_info_f)
    return run_info

def set_run_info(run_info):
    with open('run_info.json', 'r+') as run_info_f:
        run_info_f.seek(0)
        json.dump(run_info, run_info_f, indent=4)
        run_info_f.truncate()

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
    save_result(photo_pil) # tmp result photo

def simulate_algo(step):
    img = Image.open('static/uploads/photo.png')
    I1 = ImageDraw.Draw(img)
    I1.text((60, 60), str(step), fill=(255, 0, 0))
    save_result(img)

def save_result(result_pil):
    result_pil.save('static/run/recent_result.png', 'PNG')