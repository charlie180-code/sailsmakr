from datetime import datetime
from ... import db

class Authorization(db.Model):
    __tablename__ = 'authorizations'
    id = db.Column(db.Integer, primary_key=True)
    
    client_type = db.Column(db.String(20), nullable=False, default='person')

    client_identifier = db.Column(db.String, nullable=False)  # Name for person, Company name for company
    client_contact_name = db.Column(db.String)  # Only for companies
    client_phone_number = db.Column(db.String, nullable=False)
    client_email_address = db.Column(db.String)
    client_location = db.Column(db.String, nullable=False)
    
    company_nif = db.Column(db.String)
    company_rccm = db.Column(db.String)
    
    agent_name = db.Column(db.String, nullable=False)
    agent_contact = db.Column(db.String)
    agent_email = db.Column(db.String)
    
    shipping_company = db.Column(db.String, nullable=False)
    lading_bills_identifier = db.Column(db.String, nullable=False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    service_fees = db.Column(db.Float, default=0.0)
    
    supporting_docs_url = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    
    __table_args__ = (
        db.Index('ix_authorizations_client_type', 'client_type'),
        db.Index('ix_authorizations_status', 'status'),
        db.Index('ix_authorizations_date_created', 'date_created'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'client_type': self.client_type,
            'client_identifier': self.client_identifier,
            'client_contact_name': self.client_contact_name,
            'client_phone': self.client_phone_number,
            'client_email': self.client_email_address,
            'client_location': self.client_location,
            'company_nif': self.company_nif,
            'company_rccm': self.company_rccm,
            'agent_name': self.agent_name,
            'agent_contact': self.agent_contact,
            'agent_email': self.agent_email,
            'shipping_company': self.shipping_company,
            'lading_bills': self.lading_bills_identifier,
            'status': self.status,
            'date_created': self.date_created.isoformat(),
            'service_fees': self.service_fees
        }