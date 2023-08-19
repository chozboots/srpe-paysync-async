# standard
import logging
import traceback

# third-party
from quart import Blueprint, request, current_app, jsonify, render_template, redirect, url_for

# local
from database.formatters import User, Login_Info
from database import Queries
from errorHandlers.database import InsertionError
from database.utils import hash_password
from myStripe import create_customer

logger = logging.getLogger(__name__)
signup_bp = Blueprint('signup', __name__)

# -------------------
# Utility functions
# -------------------

async def email_exists(query_executor: Queries, email):
    exists = await query_executor.get_user_by_email(email)
    return bool(exists)

async def phone_exists(query_executor: Queries, phone):
    exists = await query_executor.get_user_by_phone(phone)
    return bool(exists)

async def render_error_template(message: str):
    """Utility function to render the userForm with an error message."""
    return await render_template('userForm.html', error=message), 400


# -------------------
# Template Routes
# -------------------

@signup_bp.route('/', methods=['GET'])
async def show_form():
    return await render_template('userForm.html')

@signup_bp.route('/submission_success', methods=['GET'])
async def success_page():
    return await render_template('home.html')


# -------------------
# API Routes
# -------------------

@signup_bp.route('/check-email', methods=['POST'])
async def check_email():
    json_data: dict = await request.json
    email = json_data.get('email')
    query_executor = Queries(current_app.user_database)
    
    email_already_taken = await email_exists(query_executor, email)
    return jsonify({"email_taken": email_already_taken})

@signup_bp.route('/check-phone', methods=['POST'])
async def check_phone():
    json_data: dict = await request.json
    phone = json_data.get('phone')
    query_executor = Queries(current_app.user_database)
    
    phone_already_taken = await phone_exists(query_executor, phone)
    return jsonify({"phone_taken": phone_already_taken})

@signup_bp.route('/create_customer', methods=['POST'])
async def create_customer_route():
    user_database = current_app.user_database
    
    logger.info("\n\nReceived form request.\n")

    data = await request.form

    try:
        query_executor = Queries(user_database)

        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            return await render_error_template('Passwords do not match.')
        
        async def check_exists(check_function, field, error_msg):
            if await check_function(query_executor, data.get(field)):
                return await render_error_template(error_msg)
            return None

        response = await check_exists(email_exists, 'email', 'Email already exists.')
        if response:
            return response

        response = await check_exists(phone_exists, 'phone', 'Phone number already exists.')
        if response:
            return response
        
        user = User({
            'email': data.get('email'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'phone': data.get('phone'),
            'address1': data.get('address1'),
            'address2': data.get('address2'),
            'city': data.get('city'),
            'state': data.get('state'),
            'zip_code': data.get('zip_code')
        })
        
        user_id = await query_executor.insert_user(user)

        customer_data = await create_customer(user)
        customer_id = customer_data.id

        await query_executor.update_user_customer_id(user_id, customer_id)

        hashed_password = hash_password(data.get('password'))
        login = Login_Info(user_id, hashed_password)
        
        await query_executor.insert_login(login)
        
        logger.info(f"\n\n\nUser has been inserted.\n\n")
        
        return redirect(url_for('signup.success_page')) 

    except InsertionError as e:
        constraint_name = getattr(e, 'constraint_name', 'Unknown constraint')
        field_name = getattr(e, 'field_name', 'Unknown field')
        logger.error(f"(signup) InsertionError occurred: {constraint_name} on field {field_name}")
        logger.info('\n\nEnding form request due to an InsertionError.\n\n\n')
        
        # Render the form again with an error message
        return await render_error_template(f'There was a problem creating your account. {field_name.capitalize()} already in use.')

    except Exception as e:
        tb_str = traceback.format_exception(type(e), e, e.__traceback__)
        logger.error(f"(signup) Unexpected error in route '/create_customer: <{e}> of type {type(e)}. Traceback: {''.join(tb_str)}")
        logger.info('\n\nEnding form request due to an unexpected error.\n\n\n')
        
        # Render the form again with a general error message
        return await render_error_template('This page isn\'t available right now. Please try again later.')
