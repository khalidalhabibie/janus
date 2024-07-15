from .db import db
from .utils.time_utils import get_current_time
from sqlalchemy import event, Index


class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.String(50), primary_key=True,
                         unique=True, nullable=False)
    email_subject = db.Column(db.String(120), nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    recipients = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True))
    updated_at = db.Column(
        db.DateTime(timezone=True))
    deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    expected_sent_at = db.Column(db.DateTime(timezone=True), index=True)
    exactly_sent_at = db.Column(db.DateTime(
        timezone=True), index=True, nullable=True)
    is_sent = db.Column(db.Boolean, default=False, index=True)
    is_failed = db.Column(db.Boolean, default=False, index=True)
    error_message = db.Column(db.Text, nullable=True)

    __table_args__ = (
        Index('idx_expected_sent_at_is_sent_is_failed_deleted_at',
              'expected_sent_at', 'is_sent', 'is_failed', 'deleted_at'),
    )

# Set created_at and updated_at before insert
@event.listens_for(Event, 'before_insert')
def receive_before_insert(mapper, connection, target):
    current_time = get_current_time()
    target.created_at = current_time
    target.updated_at = current_time

# Set updated_at before update
@event.listens_for(Event, 'before_update')
def receive_before_update(mapper, connection, target):
    target.updated_at = get_current_time()
