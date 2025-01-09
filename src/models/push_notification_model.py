from src import db

class PushNotification(db.Model):
    __tablename__ = 'push_notifications'

    notification_id = db.Column(db.Integer, primary_key=True)  #
    title = db.Column(db.String(255), nullable=False)  
    message = db.Column(db.Text, nullable=False)  
    schedule_date = db.Column(db.Date, nullable=False)  
    schedule_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="Active") 
    created_at = db.Column(db.DateTime, default=db.func.now()) 
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now()) 
