import random
from app import db
from app.models.assignment import Assignment
from app.models.event import Event


def assign_secret_santa(event: Event):

    participants = [u for u in event.participants if not u.is_admin]

    if len(participants) < 2:
        raise ValueError("Insufficient participants.")

    existing = Assignment.query.filter_by(event_id=event.id).first()

    if existing:
        raise ValueError("This event has already been raffled off.")

    givers = participants.copy()
    receivers = participants.copy()

    random.shuffle(receivers)

    for i in range(len(givers)):
        if givers[i].id == receivers[i].id:
            swap = (i + 1) % len(receivers)
            receivers[i], receivers[swap] = receivers[swap], receivers[i]

    for giver, receiver in zip(givers, receivers):
        assignment = Assignment(
            event_id=event.id, giver_id=giver.id, receiver_id=receiver.id
        )
        db.session.add(assignment)

    db.session.commit()
