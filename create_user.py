from database.db import SessionLocal
from database.models import User
from werkzeug.security import generate_password_hash

db = SessionLocal()

user = User(
    username="admin",
    password=generate_password_hash("admin123")
)

db.add(user)
db.commit()

print("User created")
