@dashboard_bp.route("/")
def dashboard():
    logs = get_recent_logs()
    stats = get_attack_stats()
    alerts = get_recent_alerts()  # make sure this exists

    # ✅ FIX: Convert alerts to JSON-safe format
    alerts_data = []
    for a in alerts:
        alerts_data.append({
            "attack_type": a.attack_type or "unknown",
            "severity": (a.severity or "LOW").upper(),
            "confidence": getattr(a, "confidence", 0),
            "timestamp": str(a.timestamp)
        })

    return render_template(
        "index.html",
        logs=logs,
        stats=stats,
        alerts=alerts_data   # ✅ IMPORTANT
    )
