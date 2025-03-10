from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models.general.contact import Contact
from ..models.general.subscriber import Subscriber
from ..models.general.company import Company
from ..models.general.user import User
import os
from flask_mail import Message
from .. import mail, db
from twilio.rest import Client
from . import msg
from flask_babel import gettext as _


@msg.route('/view_contacts/<int:company_id>', )
@login_required
def view_contacts(company_id):
    company = Company.query.get_or_404(company_id)
    contacts = Contact.query.filter_by(company_id=company.id)
    return render_template('dashboard/customers/view_contacts.html', contacts=contacts, company=company)


@msg.route('/messages/recent/<int:company_id>', methods=['GET'])
@login_required
def recent_messages(company_id):
    recent_messages = (
        Message.query
        .filter_by(receiver_id=current_user.id, company_id=company_id)
        .order_by(Message.timestamp.desc())
        .limit(10)
        .all()
    )

    return render_template('messages/recent_messages.html', recent_messages=recent_messages)


@msg.route('/messages/programmed', methods=['GET'])
def programmed_messages():
    # Fetch programmed messages from the database or other source
    programmed_messages = []

    # Example: fetching programmed messages from a database
    # programmed_messages = Message.query.filter_by(status='programmed').all()

    return render_template('messages/programmed_messages.html', programmed_messages=programmed_messages)

@msg.route("/mailbox/contacts/<int:company_id>")
@login_required
def get_contacts(company_id):
    
    # here we can trigger a javascript function that will
    # this function will work on input so 
    
    company = Company.query.get_or_404(company_id)
    users = User.query.filter_by(company_id=company.id).all()
    contacts = []
    for user in users:
        user_contacts = Contact.query.filter_by(user_id=user.id).all()
        for contact in user_contacts:
            contacts.append({'email': contact.email, 'name': contact.name})
    return jsonify(contacts)

@msg.route("/mailbox/new_message/<int:company_id>", methods=['GET', 'POST', 'DELETE'])
@login_required
def new_message(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        data = request.get_json()
        sender_email = data.get('email')
        receiver_email = data.get('receiver')
        message_body = data.get('message')

        sender = User.query.filter_by(email=sender_email).first()
        receiver = User.query.filter_by(email=receiver_email).first()

        if not sender or not receiver:
            return jsonify({'message': 'Expéditeur ou récepteur invalide'}), 400

        new_message = Message(
            body=message_body,
            sender_id=sender.id,
            receiver_id=receiver.id
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({'message': 'Message envoyé avec succès!'}), 200  

    return render_template('api/messages/new_message.html', company=company)


@msg.route('/send-message/<int:company_id>', methods=['POST'])
def send_email(company_id):
    company = Company.query.get_or_404(company_id)
    data = request.form

    first_name = data.get('first-name')
    last_name = data.get('last-name')
    company = data.get('company', '')
    email = data.get('email')
    phone = data.get('author_phone_number_raw')
    message_content = data.get('message')

    subject = "Soumission de formulaire de contact pour les ventes"
    sender = ("Site web AfriLog", 'noreply@afrilog.net')
    recipients = [os.environ.get('COMPANY_SALES_MANAGER')]

    body = f"""
    Vous avez une nouvelle soumission de formulaire de contact.

    Nom : {first_name} {last_name}
    Entreprise : {company}
    Email : {email}
    Téléphone : {phone}

    Message :
    {message_content}
    """

    body = body.format(first_name=first_name, last_name=last_name, company=company, email=email, phone=phone, message_content=message_content)

    try:
        msg = Message(subject, sender=sender, recipients=recipients, body=body)
        mail.send(msg)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))
    


@msg.route('/send-whatsapp-message/<int:company_id>', methods=['POST'])
def send_whatsapp_message(company_id):
    company = Company.query.get_or_404(company_id)
    account_sid = os.environ.get('TWILIO_ACCOUNT_ID_SECRET')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_phone_number = 'whatsapp:+14155238886'

    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    message_text = data.get('message')
    phone_number = data.get('phone')

    if not phone_number:
        return jsonify({'error': 'Phone number is required'}), 400

    body = f"Nom du client: {first_name}, Prénom du client: {last_name}, Message: {message_text}"

    try:

        existing_contact = Contact.query.filter_by(phone=phone_number).first()
        
        if existing_contact:
            pass
        
        else:
            new_contact = Contact(
                first_name=first_name,
                last_name=last_name,
                phone=phone_number,
                message=message_text
            )

            db.session.add(new_contact)
            db.session.commit()

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=body,
            from_=twilio_phone_number,
            to=f'whatsapp:{phone_number}'
        )

        print(message.sid)

        return jsonify({'message': 'Message sent successfully'}), 200

    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return jsonify({'error': 'Failed to send message'}), 500
    

@msg.route('/store_a_subscriber/<int:company_id>', methods=['POST'])
def subscriber_saver(company_id):
    company = Company.query.get_or_404(company_id)
    data = request.json 
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    existing_subscriber = Subscriber.query.filter_by(email=email).first()
    
    if existing_subscriber:
        return jsonify({'error': 'Contact already exists in the database'}), 400
    
    new_subscriber = Subscriber(email=email, company_id=company.id)
    
    try:
        db.session.add(new_subscriber)
        db.session.commit()
        return jsonify({'message': 'New contact successfully added in the database'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add contact: {str(e)}'}), 500
    finally:
        db.session.close()


@msg.route('/create_contact/<int:company_id>', methods=['GET', 'POST'])
@login_required
def create_contact(company_id):
    company = Company.query.get_or_404(company_id)
    if request.method == 'POST':
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        gender = data.get('gender')
        source = _('Réperoire personnel')
        message = ' '

        # check if the phone number exists
        existing_phone = Contact.query.filter_by(phone=phone, user_id=current_user.id).first()

        if existing_phone:
            return jsonify({'success': False, 'errorType': 'DuplicatePhone'}), 401
        
        # check if the email exists
        existing_email = Contact.query.filter_by(email=email, user_id=current_user.id).first()

        if existing_email:
            return jsonify({'success': False, 'errorType': 'DuplicateEmail'}), 401
        
    
        new_contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            gender=gender,
            company_id=company.id,
            source=source,
            message=message,
            user_id=current_user.id
        )

        try:
            db.session.add(new_contact)
            db.session.commit()
            return jsonify({'title' : _('Contact Ajouté'), 'message': _('Contact ajouté avec succès')}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': str(e)}), 500

    return render_template('api/customers/contacts/create_contact.html', company=company)



