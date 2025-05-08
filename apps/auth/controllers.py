from flask import render_template, request, jsonify, flash, redirect, url_for, flash, session, current_app, send_file
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash
from . import auth
import re
from ..models.general.user import User, generate_password_hash
from ..models.general.company import Company
from ..models.general.role import Role
from ..models.utils import roles_translations
from datetime import datetime
from flask_babel import _
from flask_login import login_user, logout_user
import os
from dotenv import load_dotenv
from .utils import confirm_reset_token, generate_reset_token, check_internet_connection, save_file_locally, get_company_files
from .. import oauth, db
from ..utils import save_files
from .emails.company.welcome import welcome_company
from ..utils import generate_password
from ..decorators import it_administrator_required
from .emails.password_reset_request import send_reset_email
from werkzeug.utils import secure_filename
import json

load_dotenv()


google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email',
        'prompt': 'consent'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.get_json(force=True)
        email = login_data.get('email')
        password = login_data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({'success': False, 'errorType': 'incorrectEmail'}), 401

        if not check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'errorType': 'incorrectPassword'}), 401

        company_id = user.company_id

        if company_id:
            login_user(user)
            session['company_id'] = company_id
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return jsonify({'success': True, 'company_id': company_id})

        login_user(user)
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return jsonify({'success': True})

    return render_template('auth/login.html')



@auth.route('/google_login_authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('auth.login'))

    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')

    email = user_info.data['email']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash( _('Veuillez créer un compte pour continuer'), 'error')
        return redirect(url_for('auth.signup'))

    login_user(user)

    return redirect(url_for('main.user_home'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@auth.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('auth.google_authorized', _external=True))


@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        SignUpData = request.get_json(force=True)

        first_name = SignUpData.get('firstName')
        last_name = SignUpData.get('lastName')
        email = SignUpData.get('email')
        password = SignUpData.get('password')
        confirm_password = SignUpData.get('confirmPassword')
        tools = SignUpData.get('tools', [])
        field = SignUpData.get('field')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'email_exists'})

        if password != confirm_password:
            return jsonify({'success': False, 'message': 'password_mismatch'})

        if len(password) < 8:
            return jsonify({'success': False, 'message': 'weak_password'})

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password),
            tools=json.dumps(tools),
            field_of_study=field
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True})

    return render_template("auth/signup.html")


@auth.route('/google_signup')
def google_signup():
    return google.authorize(callback=url_for('auth.google_signup_authorized', _external=True))

@auth.route('/google_signup_authorized')
def google_signup_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash('Access denied: reason={0} error={1}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('auth.signup'))

    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')

    email = user_info.data['email']
    name = user_info.data.get('name', 'User')

    user = User.query.filter_by(email=email).first()
    if user:
        flash( _('Ce compte existe déja, veuillez vous connecter'), 'error')
        return redirect(url_for('auth.login'))

    new_user = User(
        email=email, 
        first_name=name,
        last_name=name, 
        password=generate_password_hash(os.urandom(24).hex())
    )

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return redirect(url_for('main.user_home'))

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Basic validation
        if not email:
            flash(_('Veuillez entrer votre adresse e-mail.'), 'danger')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash(_('Veuillez entrer une adresse e-mail valide.'), 'danger')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                token = generate_reset_token(user)
                send_reset_email(user.email, token)
                flash(_('Un email contenant des instructions a été envoyé à {}').format(user.email), 'success')
            else:
                flash(_('Aucun compte n\'est associé à {}').format(email), 'danger')
        
        return redirect(url_for('auth.reset_password'))
    
    return render_template('auth/reset_password_request.html')

@auth.route("/reset/<token>", methods=['GET', 'POST'])
def reset_with_token(token):
    user_id = confirm_reset_token(token)

    if request.method == 'POST':
        if user_id:
            user = User.query.get(user_id)
        else:
            flash(_('Le lien de réinitialisation est invalide ou a expiré'), 'danger')
            return redirect(url_for('auth.reset_password'))
        
        confirm_password = request.form.get('confirm_password')
        password = request.form.get('password')
        if not password:
            flash(_('Votre mot de passe est requis pour continuer'), 'danger')
            return redirect(url_for('auth.reset_with_token', token=token))
        
        elif not confirm_password:
            flash(_('Veuillez confirmer votre mot de passe pour continuer'), 'danger')
            return redirect(url_for('auth.reset_with_token', token=token))

        elif not (password==confirm_password):
            flash(_('Les deux mots de passe ne correspondent pas'), 'danger')
            return redirect(url_for('auth.reset_with_token', token=token))
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        flash(_('Votre mot de passe a été réinitialisé, veuillez vous connecter'), 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/new_password.html')


@auth.route("/reset_email", methods=['GET', 'POST'])
def reset_email():
    if request.method == 'POST':
        print('This is a post request')
    return render_template("auth/reset_email.html")

@auth.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/company/register", methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        category = request.form.get('category')
        nature = request.form.get('nature')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        website_url = request.form.get('website_url')
        linkedin_url = request.form.get('linkedin_url')
        twitter_url = request.form.get('twitter_url')
        facebook_url = request.form.get('facebook_url')
        number_of_employees = request.form.get('number_of_employees')
        year_established = request.form.get('year_established')
        annual_revenue = request.form.get('annual_revenue')

        logo_file = request.files.get('logo')

        if not title:
            return jsonify({"error": "Company title is required"}), 400
        if not logo_file:
            return jsonify({"error": "Logo file is required"}), 400
        
        if check_internet_connection():
            saved_logo_url = save_files([logo_file], "company_logos")[0]
        else:
            saved_logo_filename = save_file_locally(logo_file, folder_name="static/company_logos")
            saved_logo_url = url_for('static', filename=f"company_logos/{saved_logo_filename}", _external=True)


        company = Company(
            title=title,
            description=description,
            logo_url=saved_logo_url,
            location=location,
            category=category,
            nature=nature,
            email=email,
            phone_number=phone_number,
            website_url=website_url,
            linkedin_url=linkedin_url,
            twitter_url=twitter_url,
            facebook_url=facebook_url,
            number_of_employees=number_of_employees,
            year_established=year_established,
            annual_revenue=annual_revenue
        )

        db.session.add(company)
        db.session.commit()

        password = generate_password()

        new_it_admin = User(
            email=email,
            password_hash=generate_password_hash(password),
            company_id=company.id
        )

        if company.category == 'Education':
            it_admin_role = Role.query.filter_by(name='School IT Administrator').first()
            if it_admin_role:
                new_it_admin.role = it_admin_role
        
        else:
            it_admin_role = Role.query.filter_by(name='IT Administrator').first()
            if it_admin_role:
                new_it_admin.role = it_admin_role

        db.session.add(new_it_admin)
        db.session.commit()

        if check_internet_connection():
            welcome_company(email, password)

        return jsonify({"message": "Company registered successfully!"}), 200
    
    return render_template("auth/register_company.html")




@auth.route("/manage_company_admins/<int:company_id>", methods=['GET', 'PUT', 'DELETE', 'POST'])
@it_administrator_required
def manage_company_admins(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 10
        pagination = User.query.join(Role).filter(
            User.company_id == company_id,
            Role.position.in_(['responsible', 'Sales Manager', 'agent'])
        ).paginate(page=page, per_page=per_page)


        roles = Role.query.filter(Role.position.in_([
            'responsible',
            'Sales Manager',
            'agent'
        ])).all()

        if company.category == 'Engineering':
            pipelines = Pipeline.query.filter_by(company_id=company_id).all()
            return render_template(
                'auth/general/@support_team/it_admin/admin/manage_admin.html',
                company=company,
                admins=pagination.items,
                pagination=pagination,
                roles=roles,
                pipelines=pipelines
            )

        return render_template(
            'auth/general/@support_team/it_admin/admin/manage_admin.html',
            company=company,
            admins=pagination.items,
            pagination=pagination,
            roles=roles
        )
    
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        role_id = data.get('role_id')
        password = generate_password()
        station = data.get('station')
        
        if not name or not email or not role_id:
            return jsonify(
                {
                    "title": _('Erreur'),
                    "error": _('Infos incomplètes'),
                    'confirmButtonText': _('OK')
                }
            ), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify(
                {
                    "title": _('Erreur'),
                    "error": _("Cette adresse e-mail existe déja!"),
                    'confirmButtonText': _('OK')
                }
            ), 400

        
        new_user = User(
            first_name=name,
            email=email,
            password_hash=generate_password_hash(password),
            company_id=company_id,
            pipeline_id=station
        )
        

        role = Role.query.get(role_id)
        role_name = roles_translations.get(role.name, role.name)

        db.session.add(new_user)
        db.session.commit()

        new_user.role_id = role.id
        db.session.commit()

        if check_internet_connection():
            welcome_school_admin(email, password, role_name)

        return jsonify(
            {
                "title": _('Nouvel agent ajouté!'),
                "message": _('Le nouvel agent a été ajouté!'),
                "confirmButtonText": _('OK')
            }
        ), 201

    elif request.method == 'PUT':
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email')
        role_id = data.get('role_id')

        if not user_id or not name or not email or not role_id:
            return jsonify(
                {
                    "title": _('Infos incomplètes'),
                    "error": _('Infos incomplètes'),
                    "confirmButtonText": _('OK')
                }
            ), 400

        user = User.query.get_or_404(user_id)
        user.first_name = name
        user.email = email
        user.role_id = role_id

        role = Role.query.get(role_id)
        role_name = roles_translations.get(role.name, role.name)

        db.session.commit()

        return jsonify(
            {
                "title": _('Mise à jour effectuée'),
                "message": _('Infos mises à jour!'),
                "confirmButtonText": _('OK')
            }
        ), 200

    elif request.method == 'DELETE':
        data = request.get_json()
        user_id = data.get('user_id')
        print(user_id)

        if not user_id:
            return jsonify(
                {
                    "error": _('id de l\'utilisateur introuvable')
                }
            ), 400

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return jsonify(
            {
                "title": _('Supprimé!'),
                "message": _('Agent supprimé!'),
                'confirmButtonText': _('OK')
            }
        ), 200
