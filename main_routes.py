from flask import Blueprint, render_template, jsonify, redirect, request, url_for
from sqlalchemy import or_, and_
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Cases, Engineers, Categories, Sub_Categories
from helpers import apology


main_bp = Blueprint('main',__name__)

@main_bp.route('/', methods=['GET', 'POST'])
@jwt_required()
def index():

    current_user = get_jwt_identity()
    current_engineer = Engineers.query.filter_by(email=current_user).first()

    categories = Categories.query.all()
    sub_categories = Sub_Categories.query.all()
        
    if request.method == 'POST':

        case_number = request.form.get("case_number")
        title = request.form.get("title")
        category = request.form.get("category")
        sub_category = request.form.get("sub-category")
        issue_description = request.form.get("issue_description")
        environment = request.form.get("environment")
        troubleshooting = request.form.get("troubleshooting")
        resolution = request.form.get("resolution")

        existing_case = Cases.query.filter_by(ticket_number=case_number).first()

        if existing_case and existing_case.ticket_number == case_number:

            return jsonify({'msg:' 'Case already exists'}), 401

        else:
            new_case = Cases(
                ticket_number=case_number, title=title, category=category, 
                sub_category=sub_category, issue_description=issue_description, 
                environmnet_assets=environment, troubleshooting=troubleshooting, 
                resolution=resolution
            )
            new_case.engineer = current_engineer
            new_case.save()
        
    return render_template('index.html', user=current_user, categories=categories, sub_categories=sub_categories)


@main_bp.route('/cases', methods=['GET', 'POST'])
@jwt_required()
def cases():
        
        categories = Categories.query.all()
        sub_categories = Sub_Categories.query.all()
        
        if request.method == 'POST':

            case_id = request.form.get("case_id")

            issue_description = request.form.get("issue_description")
            environment = request.form.get("environment")
            troubleshooting = request.form.get("troubleshooting")
            resolution = request.form.get("resolution")

            existing_case = Cases.query.filter_by(id=case_id).first()

            if str(existing_case.id) == case_id:

                existing_case.issue_description = issue_description
                existing_case.environmnet_assets = environment
                existing_case.troubleshooting = troubleshooting
                existing_case.resolution = resolution
                existing_case.save()
            
            else:
                return apology("Case not found, contact oscard@microsoft.com", 404)
             
    
        current_user = get_jwt_identity()
        current_engineer = Engineers.query.filter_by(email=current_user).first()

        if current_engineer is None:
             return apology("Engineer not found", 404)
    
        cases = current_engineer.case_list

    
        return render_template('cases.html', user=current_user, cases=cases, categories=categories, sub_categories=sub_categories)

@main_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete():
     
     if request.method == 'POST':
            data = request.get_json()
            case_id = data.get('id')

            case = Cases.query.filter_by(id=case_id).first()
            case.delete_case(id=case_id)
            
            return redirect(url_for('main.cases'))
     

@main_bp.route('/filter', methods=['POST'])
@jwt_required()
def filter():

    categories = Categories.query.all()
    sub_categories = Sub_Categories.query.all()

    current_user = get_jwt_identity()

    current_engineer = Engineers.query.filter_by(email=current_user).first()

    if current_engineer is None:
        return apology("Engineer not found", 404)
    
    conditions = []
    filters = []
 
    case_number = request.form.get('case_number')
    title = request.form.get('title')
    category = request.form.get('category')
    sub_category = request.form.get('sub-category')
    
    query = Cases.query.filter_by(engineer_id=current_engineer.id)

    if case_number:
        conditions.append(Cases.ticket_number.like(f'%{case_number}%'))
        filters.append(f'Case Number: {case_number}')
    if title:
        conditions.append(Cases.title.like(f'%{title}%'))
        filters.append(f'Title: {title}')
    if category != '...':
        conditions.append(Cases.category == category)
        filters.append(f'Category: {category}')
    if sub_category != '...':
        conditions.append(Cases.sub_category == sub_category)
        filters.append(f'Sub-Category: {sub_category}')

    if conditions:
        query = query.filter(and_(*conditions))
    
    cases = query.all()
    print(filters)

    return render_template('cases.html', user=current_user, cases=cases, categories=categories, sub_categories=sub_categories, filters=filters)