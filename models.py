from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, UniqueConstraint, event
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from datetime import datetime
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Engineers(db.Model):
    __tablename__ = 'engineers'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    hash = db.Column(db.String(), nullable=False)
    case_list = db.relationship('Cases', back_populates="engineer")
    __table_args__ = (UniqueConstraint('email'),)

    def __repr__(self) -> str:
        return f"Engineer {self.email}"
    
    #instance methods
    def set_password(self,password):
        self.hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.hash, password)
    
    #class methods
    @classmethod
    def check_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Cases(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    title = db.Column(db.String(), nullable=False)
    ticket_number = db.Column(db.String(), nullable=False)
    issue_description = db.Column(db.String(), nullable=True)
    environmnet_assets = db.Column(db.String(), nullable=True)
    troubleshooting = db.Column(db.String(), nullable=True)
    resolution = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime(), server_default=text("(datetime('now'))"), nullable=False)
    updated_at = db.Column(db.DateTime(), server_default=text("(datetime('now'))"), onupdate=func.now(), nullable=False)
    engineer_id = db.Column(db.Integer(), db.ForeignKey('engineers.id'), nullable=True)
    engineer = db.relationship('Engineers', back_populates="case_list")
    category = db.Column(db.String(), nullable=True)  # New category column
    sub_category = db.Column(db.String(), nullable=True)  # New sub_category column
    images = db.relationship('Images', back_populates="cases")


    def repr(self) -> str:
        return f"Case {self.title} ({self.ticket_number})"
    
    @classmethod
    def delete_case(cls, id):
        case = cls.query.get(id)
        if case:
            db.session.delete(case)
            db.session.commit()
            return True
        return False
    
    def create_case_number(self, case_number):
        self.case_number = case_number

    def create_case_description(self, issue_description):
        self.issue_description = issue_description

    def create_case_title(self, title):
        self.title = title

    def add_engineer(self, engineer):
        self.engineer = engineer

    def add_category(self, category):
        self.category = category

    def add_sub_category(self, sub_category):
        self.sub_category = sub_category
    
    def add_issue_description(self, issue_description):
        self.issue_description = issue_description
    
    def add_environmnet_assets(self, environmnet_assets):
        self.environmnet_assets = environmnet_assets

    def add_resolution(self, resolution):
        self.resolution = resolution

    def save(self):
        db.session.add(self)
        db.session.commit()
        

class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    product = db.Column(db.String(), nullable=False)

    def repr(self) -> str:
        return f"Category {self.product} ({self.sub_category.sub_type})"


class Sub_Categories(db.Model):
    __tablename__ = 'sub_types'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    sub_type = db.Column(db.String(), nullable=False)


    def repr(self) -> str:
        return f"Sub-Category {self.sub_type}"


class Images(db.Model):
    __tablename__ = 'images'
    __tablename__ = 'images'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    image_url = db.Column(db.String(), nullable=False)
    case_id = db.Column(db.Integer(), db.ForeignKey('cases.id'))
    cases = db.relationship('Cases', back_populates="images")

    def repr(self) -> str:
        return f"Image {self.id} ({self.image_url})"


def populate_categories():
    categories = [
        'Application Gateway', 'Azure Firewall', 'VNet', 'VPN Gateway', 
        'ExpressRoute', 'Azure DNS', 'Traffic Manager', 'Azure Front Door', 
        'Azure CDN', 'DDoS Protection', 'Load Balancer', 'Bastion', 
        'Azure DNS', 'Traffic Manager',  'Virtual WAN', 'Network Watcher',
        'Private Link', 'Private DNS Zones', 'Private Resolver', 'Route Server'
        ]  

    for category_name in categories:
        category = Categories.query.filter_by(product=category_name).first()
        if not category:
            category = Categories(product=category_name)
            db.session.add(category)

    db.session.commit()


def populate_subcategories():
    sub_categories = [
        '5XX Errors', '4XX Errors', 'Configuration Issues', 'How to',
        'Connectivity Issues', 'BGP Issues', 'Cert Issues', 'Peering Issues', 'Circuit Issues',
        'No ARP', '3rd party issues', 'NSG Issues', 'NAT Issues', 'TLS Issues', 'Documentation needed', 
        'Other'
        ]  

    for sub_category_name in sub_categories:
        sub_category = Sub_Categories.query.filter_by(sub_type=sub_category_name).first()
        if not sub_category:
            sub_category = Sub_Categories(sub_type=sub_category_name)
            db.session.add(sub_category)

    db.session.commit()
    




