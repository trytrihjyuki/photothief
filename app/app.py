import os
import json
import sys

from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from web_utils import *
from utils import *


UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = '1234'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
input_data = {}

@app.route('/run')
def run():

    return render_template('run.html', photo='photo.'+input_data['photo_ext'])

@app.route('/run', methods=['POST'])
def get_params():
    print("elo")
    print(get_configs())
    gowno = {"siema": 70, "elo": 420}
    set_configs(gowno)
    return redirect(url_for('run'))

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    extension_info = request.args.get('extension_info')
    dimensions_info = request.args.get('dimensions_info')
    if request.method == 'POST':
        if 'watermark_file' not in request.files or 'photo_file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload_file', extension_info=True)) # update website with information about avalible extensions
        watermark_file = request.files['watermark_file']
        photo_file = request.files['photo_file']
        watermark_ext = check_file(watermark_file)
        photo_ext = check_file(photo_file)

        # uploaded files had good extensions we can process further
        if watermark_ext is not None and photo_ext is not None:
            input_data['watermark_ext'] = watermark_ext
            input_data['photo_ext'] = photo_ext
            watermark_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'watermark.' + watermark_ext))
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'photo.' +  photo_ext))

            # save uploaded file extensions to config JSON
            with open('config.json', 'r+') as configs_f:
                configs = json.load(configs_f)
                configs['watermark_ext'] = watermark_ext
                configs['photo_ext'] = photo_ext
            set_configs(configs)
            try:
                resize_img() # we want to check img size and resize it to feasible for NN dimensions
            except ValueError:
                return redirect(url_for('upload_file', dimensions_info=True)) # We need to inform user that he needs to upload same sizes images
            return redirect(url_for('run'))
        else:
            return redirect(url_for('upload_file', extension_info=True))

    tags = {}
    if extension_info:
        tags['ext_instruction'] = True
    if dimensions_info:
        tags['dim_instruction'] = True

    return render_template('index.html', **tags)
 
if __name__ == '__main__':
    app.debug = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

