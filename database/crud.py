from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Log, Alert
from database.db import SessionLocal


# =========================
# INSERT LOG
# =========================
def insert_log(data: dict):
    session = SessionLocal()
    try:
        log = Log(**data)
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    except Exception as e:
        session.rollback()
        print(f"DB Insert Error: {e}")
        return None

    finally:
        session.close()


# =========================
# INSERT ALERT (NEW)
# =========================
def insert_alert(data: dict):
    session = SessionLocal()
    try:
        alert = Alert(**data)
        session.add(alert)
        session.commit()
        session.refresh(alert)
        return alert

    except Exception as e:
        session.rollback()
        print(f"DB Alert Insert Error: {e}")
        return None

    finally:
        session.close()


# =========================
# GET RECENT LOGS
# =========================
def get_recent_logs(limit: int = 20):
    session = SessionLocal()
    try:
        logs = (
            session.query(Log)
            .order_by(Log.timestamp.desc())
            .limit(limit)
            .all()
        )
        return logs

    except Exception as e:
        print(f"Error fetching logs: {e}")
        return []

    finally:
        session.close()


# =========================
# GET RECENT ALERTS (FIXED)
# =========================
def get_recent_alerts(limit: int = 20):
    session = SessionLocal()
    try:
        alerts = (
            session.query(Alert)
            .order_by(Alert.timestamp.desc())
            .limit(limit)
            .all()
        )
        return alerts

    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []

    finally:
        session.close()


# =========================
# GET ATTACK STATS (ENHANCED)
# =========================
def get_attack_stats():
    session = SessionLocal()
    try:
        stats = (
            session.query(Log.attack_type, func.count(Log.id))
            .group_by(Log.attack_type)
            .all()
        )

        result = {attack: count for attack, count in stats}

        # ✅ ADD SUMMARY FOR DASHBOARD
        total = sum(result.values())
        attacks = sum(v for k, v in result.items() if k != "normal")
        normal = result.get("normal", 0)

        return {
            "total": total,
            "attacks": attacks,
            "normal": normal,
            "details": result
        }

    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "total": 0,
            "attacks": 0,
            "normal": 0,
            "details": {}
        }

    finally:
        session.close()
