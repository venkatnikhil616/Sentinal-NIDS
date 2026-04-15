from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from flask_login import UserMixin
from database.db import Base


# ---------------------------
# LOG MODEL
# ---------------------------
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    protocol_type = Column(String)
    service = Column(String)
    flag = Column(String)

    src_bytes = Column(Integer)
    dst_bytes = Column(Integer)

    attack_type = Column(String)
    confidence = Column(Float)
    severity = Column(String)

    event_type = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)


# ---------------------------
# ALERT MODEL
# ---------------------------
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    attack_type = Column(String)
    severity = Column(String)
    message = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)


# ---------------------------
# USER MODEL ✅ FIXED
# ---------------------------
class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
