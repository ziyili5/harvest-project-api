from datetime import datetime

import click
from db import db
from flask.cli import with_appcontext
from models import User
from models import UserField

FIXTURES = {
    "users": [
        {"user_id": "john.doe@example.com", "first_name": "John", "last_name": "Doe"},
        {"user_id": "jane.doe@example.com", "first_name": "Jane", "last_name": "Doe"},
    ],
    "user_fields": [
        {"user_id": "john.doe@example.com", "clu": 653924, "clu_name": "FIELD-2"},
        {"user_id": "jane.doe@example.com", "clu": 658520, "clu_name": "FIELD-3"},
        {"user_id": "jane.doe@example.com", "clu": 654696, "clu_name": "FIELD-4"},
        {"user_id": "john.doe@example.com", "clu": 660881, "clu_name": "FIELD-5"},
    ],
}


@click.command("fixtures")
@with_appcontext
def fixtures_command():
    """Create sample users and user fields"""
    for user_attrs in FIXTURES["users"]:
        user = User(**user_attrs, last_login=datetime.now(),)
        db.session.add(user)
    db.session.commit()

    for user_field_attrs in FIXTURES["user_fields"]:
        user_field = UserField(**user_field_attrs)
        db.session.add(user_field)
    db.session.commit()
