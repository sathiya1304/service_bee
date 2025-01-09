import os
from flask import Blueprint
from flask import Flask, jsonify, send_from_directory
from src.controllers.dashboard_controller import fetch_counts
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/fetch')
def dashboard_fetch_controller():
    return fetch_counts()

