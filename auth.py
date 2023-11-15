from flask import Blueprint, render_template, request, redirect, session, url_for, make_response, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies, unset_access_cookies, unset_refresh_cookies
from helpers import apology
from models import Engineers
import re


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=["GET", "POST"])

def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure email was submitted
        if not email:
            return apology("must provide email", 400)
        
        # Ensure that user does not exist already
        engineer = Engineers.check_email(email=email)

        if engineer is not None:
            return apology("email already exists", 400)

        # Ensures email is valid format
        elif not re.match(r'^([\w\.]+)@(xyz\.com)$', email):
            return apology("Invalid email", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password matches confirmation
        elif password != confirmation:
            return apology("passwords don't match", 400)

        new_engineer = Engineers(email=email)
        new_engineer.set_password(password=password)
        new_engineer.save()

        return redirect("/login")

    return render_template("register.html") 


@auth_bp.route('/login', methods=["GET", "POST"])

def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        
        engineer = Engineers.check_email(email=email) # creates an instance of the engineer class

        if engineer is None:
            return apology("User doesn't exist: The email is either incorrect or empty", 400)
        
        elif engineer.check_password(password) is False or not password:
            return apology("Invalid password: Incorrect or empty password", 400)
        
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email) 

        resp = redirect(url_for('main.index'))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp
    
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    """Log user out"""

    # resp = make_response(jsonify({"logout":True}))
    resp = redirect(url_for('auth.login'))
    unset_jwt_cookies(resp)
    unset_access_cookies(resp)
    unset_refresh_cookies(resp)

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return resp