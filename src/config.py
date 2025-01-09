import os
import secrets

class Config:
    T_KEY = secrets.token_hex(16)  # Generate a random secret key for Flask
    JWT_SECRET_KEY = secrets.token_hex(16)  # Generate a random JWT secret key
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@localhost/service_app_BE'  # Adjust as needed
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Define the upload folder path

    # Ensure the upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Email configuration for Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'karthika18507@gmail.com'  # Your email for sending OTP
    MAIL_PASSWORD = 'qaljzonhvdbiovke'    # Your email password or app-specific password
    MAIL_DEFAULT_SENDER = 'karthika18507@gmail.com'  # Default sender for OTP emails
