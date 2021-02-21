from flask import Flask, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from app import app
from app.run_voice_analysis import run_voice_analysis
from datetime import datetime

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

UPLOAD_FOLDER = 'audio/audio'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return 'Hello World'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            log('request did not include a file. Sending error...')
            return 'Payload must include file', 400

        file = request.files['file']
        # if user does not select file, browser also might
        # submit an empty part without filename
        if file.filename == '':
            log('request did not include a file. Sending error...')
            return 'Payload must include file', 400
        


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            log('File upload success, running voice analysis...')
            
            try:
                data = run_voice_analysis(file.filename)
                print(data)
                log('Voice analysis success, deletin file and sending data...')
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[0] + '.TextGrid'))
                return jsonify(data), 200

            except Exception as e:
                log('Voice analysis error. Deleting file and sending error...', e)
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[0] + '.TextGrid'))
                return 'Voice analysis error', 500

        else:
            # file is not allowed
            log('request file is not .wav, sending error...')
            return 'Payload must be a .wav file', 400

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


def log(s, *args):
    print('[', datetime.now().strftime("%d/%m/%Y %H:%M:%S"), '] UPLOAD:', s, *args)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
