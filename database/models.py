from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database.db import Base


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    # Traffic data
    protocol_type = Column(String)
    service = Column(String)
    flag = Column(String)

    src_bytes = Column(Integer)
    dst_bytes = Column(Integer)

    # Detection results
    attack_type = Column(String)
    confidence = Column(Float)
    severity = Column(String)

    # ✅ REQUIRED FIX
    event_type = Column(String)

    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    attack_type = Column(String)
    severity = Column(String)
    message = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)
