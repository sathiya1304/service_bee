import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.vendor_register_controller import add_vendor_register,update_vendor_bank_details,update_vendor_images,update_vendor_basic_details
vendor_register_bp = Blueprint('vendor_register', __name__, url_prefix='/vendor_register')




#vendorLogin
@vendor_register_bp.route('/', methods=['POST'])
def add_vendor_register_controller():
    return add_vendor_register()

# Vendor Bank Details Update
@vendor_register_bp.route('/update_bank_details', methods=['PUT'])
def update_vendor_bank_details_controller():
    return update_vendor_bank_details()

# Vendor Image Update
@vendor_register_bp.route('/update_images', methods=['PUT'])
def update_vendor_images_controller():
    return update_vendor_images()  # Call the update_vendor_images function

# Vendor Basic Details Update
@vendor_register_bp.route('/update', methods=['PUT'])
def update_vendor_basic_details_controller():
    return update_vendor_basic_details()