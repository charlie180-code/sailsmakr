from flask import  make_response, render_template, current_app
from io import BytesIO
import qrcode
from datetime import datetime
from flask_babel import gettext as _
from weasyprint import HTML
from ..models.general.company import Company
import base64
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
import os
import requests
from sqlalchemy.orm import joinedload
from ..models.general.file import File


def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')

    qr_code_io = BytesIO()
    qr_img.save(qr_code_io, format='PNG')
    qr_code_io.seek(0)

    return qr_code_io


def generate_reset_token(user, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps({'reset': user.id}, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_reset_token(token, expiration=3600):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except:
        return False
    return data['reset']


def save_file_locally(file, folder_name="static"):
    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.root_path, folder_name, filename)
    file.save(file_path)
    return filename


def check_internet_connection():
    url = "https://www.google.com"
    timeout = 8
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False
    

def get_company_files(company_id, user_id):
    """
    Retrieve all files associated with a specific company and user.
    """
    # Query all files that are associated with the given company_id and user_id
    files = File.query.filter_by(company_id=company_id, user_id=user_id).all()
    
    return files
