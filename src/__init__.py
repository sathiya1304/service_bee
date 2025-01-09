from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail  # Import Mail from flask_mail

# Initialize extensions outside of the function
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('src.config.Config')  # Load config from the Config class

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # Initialize Mail extension
    CORS(app)  # Enable CORS for the app

    # Import and register blueprints
    from src.routes.vendor_login import vendor_login_bp
    from src.routes.vendor_register_routes import vendor_register_bp
    from src.routes.category import category_bp
    from src.routes.products import product_bp
    from src.routes.order_details_routes import order_details_bp
    from src.routes.discount_routes import discount_bp
    from src.routes.dashboard import dashboard_bp
    from src.routes.push_notification import push_notification_bp
    from src.routes.otp_email_routes import otp_email_bp
    

    # Register blueprints to the app
    app.register_blueprint(vendor_login_bp)
    app.register_blueprint(vendor_register_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_details_bp)
    app.register_blueprint(discount_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(push_notification_bp)
    app.register_blueprint(otp_email_bp)

    return app
