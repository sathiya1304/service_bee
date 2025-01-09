import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.otp_controller import generate_otp_controller, validate_otp_controller
otp_email_bp = Blueprint('otp_email', __name__, url_prefix='/otp_email')

#vendorLogin
@otp_email_bp.route('/generate_otp', methods=['POST'])
def add_otp_email_controller():
    return generate_otp_controller()

@otp_email_bp.route('/validate_otp', methods=['POST'])
def validate_otp_email_controller():
    return validate_otp_controller()

