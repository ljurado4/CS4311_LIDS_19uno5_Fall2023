# File: db_utils.py
#
# Description: Sets up functions related to the database.
#
# @ Author:
# @ Modifier: Lizbeth Jurado

from . import db
from .models import Alert

def add_alert(level, IP, Port, description):
    alert = Alert(level=level, IP=IP, Port=Port, description=description)
    db.session.add(alert)
    db.session.commit()

def get_all_alerts():
    return Alert.query.all()

def get_alert_by_id(alert_id):
    return Alert.query.get(alert_id)
