from flask import Blueprint, render_template, request, send_file
from flask_login import login_required, current_user
from .signature import signature_extractor
from . import db
import io
import cv2
import numpy as np


main = Blueprint('main', __name__)


UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':

        if 'file' not in request.files:
            return render_template('profile.html', msg='No file selected')
        file = request.files['file']
        if file.filename == '':
            return render_template('profile.html', msg='No file selected')

        if file and allowed_file(file.filename):

            
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            extracted_binary = signature_extractor(img)

            return send_file(io.BytesIO(extracted_binary), attachment_filename='result.jpg', mimetype='image/jpg')
    elif request.method == 'GET':
        return render_template('profile.html')