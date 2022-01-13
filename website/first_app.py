import os

from flask import Flask, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

from web_utils import *

app = Flask(__name__)
  
UPLOAD_FOLDER = '../data/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/run')
def run(name=None):
    return 'RUN ALGO' 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    correct_info = request.args.get('correct_info')
    if request.method == 'POST':
        if 'watermark_file' not in request.files or 'photo_file' not in request.files:
            flash('No file part')
            return redirect(url_for('upload_file', correct_info=True))
        watermark_file = request.files['watermark_file']
        photo_file = request.files['photo_file']
        #if watermark_file.filename == '' or photo_file.filename == '': # user send empty file
        #    flash('No selected file')
        #    return redirect(url_for(''))
        watermark_ext = check_file(watermark_file)
        photo_ext = check_file(photo_file)
        print(watermark_ext)
        print(photo_ext)
        if watermark_ext is not None and photo_ext is not None:
            print("gowno w dupie")
            watermark_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'watermark.' + watermark_ext))
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'input.' + photo_ext))
            return redirect(url_for('run'))

    if correct_info:
        instruction = '''
            <center>
                Add correct files of input picture and watermark. Available extensions are: .png, .jpg, .jpeg. 
            </center>
        '''
    else:
        instruction = ''

    return '''
    <!doctype html>
    <title>Photothief</title>
    <center>
    <h1>Welcome to Photothief</h1>
    </center>
    <center> Upload watermarked photo and file with this watermarked to unmark it. </center>
    <br style="line-height:10"> 
    <form method=post enctype=multipart/form-data>
        <center>
            Watermarked photo:
            <input type=file name=photo_file>
        </center>
        <br style="line-height:10"> 
        <center>
            Watermark:
            <input type=file name=watermark_file>
        </center>
        <br style="line-height:5"> 
        <center>
            Upload all files
            <input type=submit value=Upload>
        </center>
    ''' + instruction + '''</form>'''
 
app.secret_key = '1234'
if __name__ == '__main__':
    app.debug = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

