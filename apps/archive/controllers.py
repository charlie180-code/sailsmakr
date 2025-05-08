from flask import request, render_template, jsonify, redirect, url_for, flash, abort, make_response, current_app
from datetime import datetime
from flask_login import login_required, current_user
from . import archive
from ..models.general.folder import Folder
from ..models.general.file import File
from ..models.general.company import Company
from ..models.general.user import User
from ..models.general.role import Role
from ..utils import save_files
from .. import db
from math import ceil
from flask_babel import gettext as _
from dotenv import load_dotenv
import os
from .emails.notify_folder import notify_for_new_folder, notify_for_deleted_folder, notify_users_about_new_files
from firebase_admin import storage
from ..user.support_team.business.insights import get_relevant_urls_for_company, get_data_size_for_company
from ..models.general.user import User, generate_password_hash
import weasyprint

load_dotenv()

@archive.route("/folders/<int:company_id>", methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def folders(company_id):
    company = Company.query.get_or_404(company_id)
    category = company.category

    if request.method == 'GET':

        page = request.args.get('page', 1, type=int)
        folders = Folder.query.filter_by(company_id=company.id).all()

        return render_template(
            f"dashboard/@support_team/{category.lower()}/folders.html",
            folders=folders, 
            company=company,
            page=page
        )

    if request.method == 'POST':
        data = request.json
        new_folder = Folder(
            name=data['folder_name'],
            description=data.get('folder_description', ''),
            type=data.get('folder_type', ''),
            client=data.get('client', ''),
            deadline=datetime.fromisoformat(data['deadline']),
            company_id=company.id
        )


        if category == 'Shipping':
            new_folder.transport = data.get('transport', '')
            new_folder.weight = data.get('weight', '')
            new_folder.bills_of_ladding = data.get('bills_of_ladding', '')

        elif category == 'Engineering':
            new_folder.project_location = data.get('project_location', '')
            new_folder.project_manager = data.get('project_manager', '')
            new_folder.project_phase = data.get('project_phase', '')
            new_folder.budget = data.get('budget', 0.0)
            new_folder.contractor = data.get('contractor', '')
            new_folder.materials_used = data.get('materials_used', '')
            new_folder.permits_approved = data.get('permits_approved', False)
            new_folder.species_studied = data.get('species_studied', '')
            new_folder.experiment_date = datetime.fromisoformat(data.get('experiment_date', datetime.utcnow().isoformat()))
            new_folder.lab_technician = data.get('lab_technician', '')
            new_folder.sample_storage = data.get('sample_storage', '')
            new_folder.biosafety_level = data.get('biosafety_level', 1)
            new_folder.voltage = data.get('voltage', 0.0)
            new_folder.current = data.get('current', 0.0)
            new_folder.circuit_diagram = data.get('circuit_diagram', '')
            new_folder.compliance_standards = data.get('compliance_standards', '')
            new_folder.pipe_material = data.get('pipe_material', '')
            new_folder.water_pressure = data.get('water_pressure', 0.0)
            new_folder.plumbing_diagram = data.get('plumbing_diagram', '')
            new_folder.pcb_layout = data.get('pcb_layout', '')
            new_folder.components_list = data.get('components_list', '')
            new_folder.firmware_version = data.get('firmware_version', '')

            

        db.session.add(new_folder)
        db.session.commit()


        notify_for_new_folder(
            company_name=company.title,
            folder_name=new_folder.name,
            deadline=new_folder.deadline,
            company_id=company.id
        )
        

        return jsonify({
            'title': _('Nouveau dossier ajouté'),
            'success': True,
            'message': _(f"Le dossier N°{new_folder.id} vient d\'être crée"),
            'confirmButtonText': _('OK'),
        }), 201


    if request.method == 'DELETE':
        data = request.json
        folder_id = data['id']
        folder = Folder.query.get(folder_id)
        if folder:
            company = Company.query.get(folder.company_id)
            db.session.delete(folder)
            db.session.commit()

            notify_for_deleted_folder(
                company_name=company.title, 
                folder_name=folder.name, 
                folder_id=folder_id, 
                company_id=folder.company_id
            )

            return jsonify({
                'title': _('Supprimé'),
                'message': _(f"Le dossier N°{folder_id} vient d\'être supprimé"),
                'confirmButtonText': _('OK')
            }), 200
        else:
            return jsonify({
                'title': _('Dossier introuvable'),
                "error": _('Dossier introuvable')
            }), 404


@archive.route('/search_folders_files/<int:company_id>', methods=['GET'])
@login_required
def search_folders_files(company_id):

    placeholder_url = current_app.config.get('PLACEHOLDER_STATIC_URL')

    company = Company.query.get_or_404(company_id)
    query = request.args.get('query', '')
    
    folders = Folder.query.filter(
        Folder.name.ilike(f'%{query}%'),
        Folder.company_id == company.id
    ).all()
    
    files = File.query.join(Folder).filter(
        File.label.ilike(f'%{query}%'),
        Folder.company_id == company.id
    ).all()
    
    results = []
    
    for folder in folders:
        results.append({
            'label': folder.name,
            'type': 'Folder',
            'icon': '<i class="bi bi-folder"></i>'
        })
    
    results = []

    for file in files:
        ext = file.filepath.split('.')[-1].lower()
        icon = ''
        if ext in ['pdf']:
            icon = f'<img src="{placeholder_url}pdf.png" alt="{file.label}" class="img-thumbnail me-2 custom-thumbnail" style="width: 50px;">'
        elif ext in ['jpg', 'jpeg', 'png']:
            icon = f'<img src="{placeholder_url}image.png" alt="{file.label}" class="img-thumbnail me-2 custom-thumbnail" style="width: 50px;">'
        else:
            icon = '<i class="bi bi-file-earmark"></i>'

        results.append({
            'label': file.label,
            'uploaded_at': file.uploaded_at.strftime('%Y-%m-%d %H:%M'),
            'url': file.filepath,
            'type': ext.upper(),
            'icon': icon,
            'folder_name': file.folder.name
        })


    return jsonify({'results': results})



@archive.route('/folders/<int:folder_id>/close/<int:company_id>', methods=['PUT'])
@login_required
def close_folder(folder_id, company_id):
    try:
        folder = Folder.query.get_or_404(folder_id)
        company = Company.query.get_or_404(company_id)
        folder.status = True 
        db.session.commit()

        """
        warn people when a folder
        status has been changed
        send a notification when 
        a folder is changed
        """

        return jsonify(
            {
                'title': _(f"Dossier N°{folder_id} fermé"),
                'message': _(f"Le dossier N°{folder_id} vient d\'être fermé"),
                'confirmButtonText': _('OK')
            }
        ), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to close folder: {str(e)}'}), 500


@archive.route('/save_folder_files/<int:folder_id>/<int:company_id>', methods=['POST'])
@login_required
def save_folder_files(folder_id, company_id):
    company = Company.query.get_or_404(company_id)
    folder = Folder.query.get_or_404(folder_id)
    folder_title = folder.name

    files = request.files.getlist('files[]')
    labels = request.form.getlist('labels[]')

    if len(files) != len(labels):
        return jsonify({
            'title': _('Erreur'),
            'error': _('Le nombre de labels et les fichiers ne correspondent pas'),
            'confirmButtonText': _('OK')
        }), 400

    saved_files = save_files(files, "client_folder")

    for i, file_url in enumerate(saved_files):
        new_file = File(
            label=labels[i],
            filepath=file_url,
            folder_id=folder.id
        )
        db.session.add(new_file)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'title': _('Erreur'),
            'error': _('Une erreur est survenue lors de la sauvegarde des fichiers'),
            'confirmButtonText': _('OK')
        }), 500

    notify_users_about_new_files(
        company=company, 
        folder=folder, 
        files=files, 
        labels=labels
    )

    return jsonify({
        'title': _('Fichiers sauvegardés'),
        'message': _(f"Le(s) fichier(s) ont été sauvegardé(s) dans {folder_title}"), 
        'files': saved_files,
        'confirmButtonText': _('OK')
    })



@archive.route('/get_folders_list/<int:company_id>', methods=['GET'])
def get_folders(company_id):
    company = Company.query.get_or_404(company_id)
    folders = Folder.query.filter_by(company_id=company.id).all()
    folder_list = [{
        'id': folder.id,
        'description': folder.description,
        'client': folder.client,
        'bills_of_ladding': folder.bills_of_ladding,
    } for folder in folders]
    return jsonify(folder_list)

    
@archive.route("/company_disk_usage/<int:company_id>", methods=['GET', 'POST'])
@login_required
def company_disk_usage(company_id):
    company = Company.query.get_or_404(company_id)
    if not current_user.is_sailsmakr_sales_director():
        abort(403)

    bucket = storage.bucket()
    blobs = list(bucket.list_blobs())  # Convert the iterator to a list immediately

    companies = Company.query.all()
    company_disk_usages = []

    for company in companies:
        total_size = 0

        relevant_urls = get_relevant_urls_for_company(company.id)

        # Process each blob
        for blob in blobs:
            blob_url = f"https://storage.googleapis.com/afrilog-797e8.appspot.com/{blob.name}"

            # If the blob's URL is in the relevant URLs for this company, add its size
            if blob_url in relevant_urls:
                total_size += blob.size

        # Add text data size
        data_size = get_data_size_for_company(company.id)
        print(data_size)
        total_size += data_size

        # Store the company name and its total disk usage in MB
        company_disk_usages.append({
            'company_id': company.id,
            'company_name': company.title,
            'total_size_mb': total_size / (1024 * 1024)  # Convert to MB
        })

    # Sort by disk usage (optional)
    company_disk_usages.sort(key=lambda x: x['total_size_mb'], reverse=True)

    selected_company_id = request.args.get('company_id', default=None, type=int)

    # Filter the disk usage data based on the selected company
    if selected_company_id:
        company_disk_usages = [data for data in company_disk_usages if data['company_id'] == selected_company_id]

    return render_template(
        "dashboard/@support_team/company_disk_usage.html", 
        company_disk_usages=company_disk_usages,
        companies=companies,
        company=company
    )
