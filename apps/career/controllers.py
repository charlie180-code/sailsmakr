from flask import render_template, request, jsonify, flash, redirect, url_for, abort, current_app, send_file
from datetime import datetime
from flask_login import login_required, current_user
from . import career
from ..models.general.user import User
from ..models.general.role import Role
from ..models.general.employee import Employee
from ..models.general.company import Company
from ..models.general.file import File
import os
from .. import db
from ..utils import save_files
from flask_babel import _
from ..decorators import customer_required
from werkzeug.utils import secure_filename
from datetime import datetime
from ..auth.utils import check_internet_connection, save_file_locally
from .utils import generate_excel, generate_pdf, generate_qr_code, save_qr_code_to_static, generate_badge


@career.route("/careers/employees_table/<int:company_id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def employee_table(company_id):
    company = Company.query.get_or_404(company_id)
    if not current_user.is_responsible():
        abort(403)

    if request.method == 'GET':
        pipeline_id = request.args.get('pipeline_id', type=int)


        employees_query = User.query.join(Role).filter(
            User.company_id == company_id,
            ~Role.position.in_(['customer'])
        )

        page = request.args.get('page', 1, type=int)
        per_page = 10
        pagination = employees_query.paginate(page=page, per_page=per_page, error_out=False)
        employees = pagination.items

        return render_template(
            'dashboard/@support_team/employees_listing.html',
            employees=employees,
            pagination=pagination,
            selected_pipeline=pipeline_id,
            company=company
        )
    
    elif request.method == "PUT":
        data = request.form
        employee_id = data.get('employee_id')
        employee = User.query.filter_by(id=employee_id, company_id=company_id).first()
        if not employee:
            return jsonify({'error': _('L\'employé n\'existe pas')}), 404

        profile_picture = request.files.get('profile_picture')
        if profile_picture:
            company_folder = 'user_profile_pictures'
            local_folder = os.path.join(current_app.root_path, 'static', company_folder)
            
            if not os.path.exists(local_folder):
                os.makedirs(local_folder)
            
            if check_internet_connection():
                saved_profile_image_filename = save_files([profile_picture], company_folder)[0]
                saved_profile_image_url = saved_profile_image_filename
            else:
                saved_profile_image_filename = save_file_locally(profile_picture, local_folder)
                saved_profile_image_url = url_for('static', filename=f"{company_folder}/{saved_profile_image_filename}", _external=True)
            
            employee.profile_picture_url = saved_profile_image_url

        uploaded_files = request.files.getlist('uploaded_files')
        company_user_files_folder = f"company_user_files/{company_id}/"
        local_files_folder = os.path.join(current_app.root_path, 'static', company_user_files_folder)

        if not os.path.exists(local_files_folder):
            os.makedirs(local_files_folder)

        for file in uploaded_files:
            if file:
                if check_internet_connection():
                    saved_file_filename = save_files([file], company_user_files_folder)[0]
                    saved_file_url = saved_file_filename
                else:
                    saved_file_filename = save_file_locally(file, local_files_folder)
                    saved_file_url = url_for('static', filename=f"{company_user_files_folder}/{saved_file_filename}", _external=True)

                new_file = File(
                    label=file.filename,
                    filepath=saved_file_url,
                    folder_id=None,
                    user_id=employee.id,
                    company_id=company_id
                )
                db.session.add(new_file)



        employee.first_name = data.get('firstName', employee.first_name)
        employee.last_name = data.get('lastName', employee.last_name)
        employee.role.name = data.get('role', employee.role.name)
        employee.registration_number = data.get('registration_number', employee.registration_number)
        employee.social_security_number = data.get('social_security', employee.social_security_number)
        employee.service_name = data.get('service_name', employee.service_name)
        employee.emergency_contact_phone = data.get('emergency_contact', employee.emergency_contact_phone)
        employee.certifications = data.get('certifications', employee.certifications)
        employee.bank_name = data.get('bank_name', employee.bank_name)
        employee.bank_account_number = data.get('bank_account_number', employee.bank_account_number)

        if company.category in ['Education', 'Shipping', 'Engeneering']:
            arrival_date = data.get('arrival_date', None)
            leaving_date = data.get('leaving_date', None)

            if arrival_date:
                try:
                    employee.arrival_date = datetime.strptime(arrival_date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError("Invalid format for arrival_date. Expected 'YYYY-MM-DD'.")

            if leaving_date:
                try:
                    employee.leaving_date = datetime.strptime(leaving_date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError("Invalid format for leaving_date. Expected 'YYYY-MM-DD'.")

            employee.transport_company = data.get('transport_company', employee.transport_company)

        def parse_date(date_str):
            if date_str and isinstance(date_str, str):
                try:
                    return datetime.strptime(date_str, '%Y-%m-%d')
                except ValueError:
                    return None
            return None
        
        employee.contract_start_date = parse_date(data.get('contract_start_date', employee.contract_start_date))
        employee.contract_end_date = parse_date(data.get('contract_end_date', employee.contract_end_date))
        employee.employment_terms = data.get('employment_terms', employee.employment_terms)
        employee.address = data.get('address', employee.address)

        employee.gender = data.get('gender', employee.gender)
        employee.email = data.get('email', employee.email)
        employee.place_of_birth = data.get('place_of_birth', employee.place_of_birth)

        employee.date_of_birth = parse_date(data.get('date_of_birth', employee.date_of_birth))

        employee.contract_start_date = employee.contract_start_date if isinstance(employee.contract_start_date, datetime) else None
        employee.contract_end_date = employee.contract_end_date if isinstance(employee.contract_end_date, datetime) else None
        employee.date_of_birth = employee.date_of_birth if isinstance(employee.date_of_birth, datetime) else None
        employee.current_location = data.get('current_location', employee.current_location)

        db.session.commit()
        return jsonify({
            'title': _('Mise à jour effectuée'),
            'message': _('Les informations de l\'employé ont été mises à jour avec succès'),
            'confirmButtonText': _('OK')
        }), 200