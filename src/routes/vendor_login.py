import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.vendor_login import vendor_login_controller
vendor_login_bp = Blueprint('vendor_login', __name__, url_prefix='/vendor_login')

#vendorLogin
@vendor_login_bp.route('/', methods=['POST'])
def fetch_vendor_login_controller():
    return vendor_login_controller()

