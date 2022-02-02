import json
import torch
import numpy as np

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
        configs['cuda'] = False # GOWNO DO WYJEBANIA
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
    watermark_pil = Image.open('static/uploads/watermark.' + watermark_ext).convert('RGB')
    photo_pil = Image.open('static/uploads/photo.' + photo_ext).convert('RGB')
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

### neural network part ###

def generate_noise(depth, size, noise_type, factor=0.1):
    if noise_type == 'normal':
        return torch.randn(1, depth, size[0], size[1]) * factor
    elif noise_type == 'uniform':
        return torch.rand(1, depth, size[0], size[1]) * factor

'''
PIL: W x H x C [0...255]
array: C x W x H [0...1]
tensor: C x W x H [0...1]
'''

def pil_to_np(x): ##########
    x = np.array(x) #########3
    if len(x.shape) == 3:
        x = x.transpose(2,0,1) ##########
    else:
        assert False
    return x.astype(np.float32) / 255. ###############

def np_to_pil(x):
    print(x.shape)
    return Image.fromarray((x * 255.).transpose(1,2,0).astype('uint8'), 'RGB')

def tensor_to_np(x):
    return x.detach().cpu().numpy()

def np_to_tensor(x):
    return torch.from_numpy(x)[None, :]