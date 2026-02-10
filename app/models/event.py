from app import db

event_participants = db.Table(
    "event_participants",
    db.Column("event_id", db.Integer, db.ForeignKey("events.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    is_finished = db.Column(db.Boolean, default=False, nullable=False)

    participants = db.relationship(
        "User",
        secondary=event_participants,
        backref=db.backref("events", lazy="select"),
    )

    @property
    def assignments(self):
        from app.models.assignment import Assignment

        return Assignment.query.filter_by(event_id=self.id)

    @property
    def is_draw_done(self):
        from app.models.assignment import Assignment

        return Assignment.query.filter_by(event_id=self.id).count() > 0
