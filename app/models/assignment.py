from app import db
from app.models.user import User


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)

    giver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    poem = db.Column(db.Text, nullable=True)

    # ---------- RELATIONSHIPS ----------
    giver = db.relationship(User, foreign_keys=[giver_id], backref="given_assignments")

    receiver = db.relationship(
        User, foreign_keys=[receiver_id], backref="received_assignments"
    )

    @property
    def event(self):
        from app.models.event import Event

        return Event.query.get(self.event_id)
