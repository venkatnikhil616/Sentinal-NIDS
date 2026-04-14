import os
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

from database.crud import get_recent_logs, get_attack_stats


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder=os.path.join(BASE_DIR, "dashboard/templates")
)


# ---------------------------
# MAIN DASHBOARD
# ---------------------------
@dashboard_bp.route("/")
@login_required
def dashboard():
    logs = get_recent_logs()
    stats = get_attack_stats()

    return render_template(
        "index.html",
        logs=logs,
        stats=stats
    )


# ---------------------------
# REAL-TIME DATA API
# ---------------------------
@dashboard_bp.route("/data")
@login_required
def dashboard_data():
    logs = get_recent_logs()
    stats = get_attack_stats()

    return jsonify({
        "logs": [
            {
                "attack_type": log.attack_type,
                "confidence": log.confidence,
                "timestamp": str(log.timestamp)
            }
            for log in logs
        ],
        "stats": stats
    })
