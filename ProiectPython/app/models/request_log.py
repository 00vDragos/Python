from datetime import datetime
from app.core.extensions import db


class RequestLog(db.Model):
    __tablename__ = "request_logs"

    id = db.Column(db.Integer, primary_key=True)
    operation = db.Column(db.String(50), nullable=False)
    input_data = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_user_requestlog"),
        nullable=False
    )
    user = db.relationship("User", backref="request_logs")

    def __repr__(self):
        return f"<RequestLog {self.operation}({self.input_data}) = {self.result}>"
