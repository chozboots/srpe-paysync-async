# standard
import logging
import traceback

# third-party
from quart import Blueprint, jsonify, request, current_app
from quart_jwt_extended import create_access_token
from quart_jwt_extended import jwt_required, get_jwt_identity
from quart_jwt_extended.exceptions import NoAuthorizationError, WrongTokenError, RevokedTokenError, FreshTokenRequired, JWTExtendedException

# local
from database import Queries
from database.formatters import format_value
from database.utils import check_password
from errorHandlers.login import LoginError


logger = logging.getLogger(__name__)

dashboard_bp = Blueprint('dashboard_bp', __name__)


@dashboard_bp.route('/login', methods=['POST'])
async def login_route():
    # get shared database
    user_database = current_app.user_database
    
    # get form data
    data = await request.get_json()

    logger.info(f"Login attempt by user: {format_value(data['email'])}")

    try:
        query_executor = Queries(user_database)

        attempt_email = format_value(data['email'])
        user_id = await query_executor.get_user_id(attempt_email)

        attempt_password = data['password']
        user_data = await query_executor.get_login_info(user_id)
        real_password = user_data['password_hash']

        valid_login = check_password(attempt_password, real_password)

        if not valid_login:
            raise LoginError("Invalid email or password.")

        # Further processes if login is successful
        # Create a JWT token if the login is successful
        access_token = create_access_token(identity=attempt_email)

        response = {
            'message': 'Login successful.',
            'access_token': access_token
        }

        logger.info(f"User logged in successfully: {format_value(data['email'])}")

        return jsonify(response)

    except LoginError as e:
        logger.error(f"(dashboard) LoginError occurred: {str(e)}")
        return jsonify({'error': 'LoginError', 'message': 'Invalid email or password.'}), 401

    except Exception as e:
        tb_str = traceback.format_exception(type(e), e, e.__traceback__)
        logger.error(f"(dashboard) Unexpected error in route '/login': <{e}> of type {type(e)}. Traceback: {''.join(tb_str)}")
        return jsonify({'error': 'UnexpectedError', 'message': 'This page isn\'t available right now. Please try again later.'}), 500


@dashboard_bp.route('/user_dashboard', methods=['GET'])
@jwt_required  # This ensures that the user is authenticated
async def user_dashboard():
    current_user_email = get_jwt_identity()  # Get the identity of the current user
    try:
        query_executor = Queries(current_app.user_database)
        user_id = await query_executor.get_user_id(email=current_user_email)
        profile_data: dict = await query_executor.get_profile_info(user_id)
        
        profile = {
            'email': profile_data.get('email'),
            'first_name': profile_data.get('first_name'),
            'last_name': profile_data.get('last_name'),
            'phone': profile_data.get('phone'),
            'address1': profile_data.get('address1'),
            'address2': profile_data.get('address2'),
            'city': profile_data.get('city'),
            'state': profile_data.get('state'),
            'zip_code': profile_data.get('zip_code')
        }

        return jsonify(profile)

    except WrongTokenError:
        logger.error("(dashboard) Invalid token")
        return jsonify({'error': 'InvalidToken', 'message': 'Invalid token. Please log in again.'}), 401
    
    except RevokedTokenError:
        logger.error("(dashboard) Revoked token attempt")
        return jsonify({'error': 'RevokedToken', 'message': 'Token has been revoked. Please log in again.'}), 401

    except FreshTokenRequired:
        logger.error("(dashboard) Fresh token required")
        return jsonify({'error': 'NonFreshToken', 'message': 'Please refresh your token and try again.'}), 401

    except NoAuthorizationError:
        logger.error("(dashboard) No token provided")
        return jsonify({'error': 'NoToken', 'message': 'Token not provided. Please log in.'}), 401

    # Add other JWT-specific exceptions here if needed
    except JWTExtendedException as e:
        logger.error(f"(dashboard) JWT Error: {str(e)}")
        return jsonify({'error': 'JWTError', 'message': str(e)}), 401
    
    except UnicodeDecodeError:
        logger.error("(dashboard) Token decoding error. Possibly a corrupted token.")
        return jsonify({'error': 'TokenDecodeError', 'message': 'Invalid or corrupted token. Please log in again.'}), 401

    except Exception as e:
        tb_str = traceback.format_exception(type(e), e, e.__traceback__)
        logger.error(f"(dashboard) Unexpected error in route '/user_dashboard': <{e}> of type {type(e)}. Traceback: {''.join(tb_str)}")
        return jsonify({'error': 'UnexpectedError', 'message': 'Unable to fetch user data. Please try again later.'}), 500

