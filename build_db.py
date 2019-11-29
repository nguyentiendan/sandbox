import os
from config import db
from model import User

# Data to initialize database with
USER = [
    {"uid": "12312312", "fullname": "Dan Nguyen"},
    {"uid": "23423412", "fullname": "Bill Gate"},
    {"uid": "32342112", "fullname": "Tim Cook"},
]

# Delete database file if it exists currently
if os.path.exists("guide.db"):
    os.remove("guide.db")

# Create the database
db.create_all()

# iterate over the USER structure and populate the database
for user in USER:
    u = User(uid=user.get("uid"), fullname=user.get("fullname"))
    db.session.add(u)

db.session.commit()

