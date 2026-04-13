import os
from flask import Blueprint, render_template
from database.crud import get_recent_logs, get_attack_stats

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    template_folder=os.path.join(BASE_DIR, "dashboard/templates"),
    static_folder=os.path.join(BASE_DIR, "dashboard/static"),
    static_url_path="/dashboard/static"
)


@dashboard_bp.route("/")
def dashboard():
    logs = get_recent_logs()
    stats = get_attack_stats()

    return render_template(
        "index.html",
        logs=logs,
        stats=stats
    )
