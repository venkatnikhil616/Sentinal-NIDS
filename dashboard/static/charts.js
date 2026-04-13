// INITIAL DATA FROM TEMPLATE

const logsData = window.logsData || [];
const alertsData = window.alertsData || [];

// PROCESS DATA

// Count normal vs attacks
let normalCount = 0;
let attackCount = 0;

logsData.forEach(log => {
    if (log.attack_type === "normal") {
        normalCount++;
    } else {
        attackCount++;
    }
});

// Count severity
let severityCounts = {
    low: 0,
    medium: 0,
    high: 0
};

alertsData.forEach(alert => {
    const sev = (alert.severity || "").toLowerCase();
    if (severityCounts.hasOwnProperty(sev)) {
        severityCounts[sev]++;
    }
});

// TRAFFIC PIE CHART

const trafficCtx = document.getElementById("trafficChart");

if (trafficCtx) {
    new Chart(trafficCtx, {
        type: "doughnut",
        data: {
            labels: ["Normal", "Attack"],
            datasets: [{
                data: [normalCount, attackCount],
                backgroundColor: ["#22c55e", "#ef4444"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: "#e2e8f0"
                    }
                }
            }
        }
    });
}

// ALERT SEVERITY BAR CHART

const alertCtx = document.getElementById("alertChart");

if (alertCtx) {
    new Chart(alertCtx, {
        type: "bar",
        data: {
            labels: ["Low", "Medium", "High"],
            datasets: [{
                label: "Alerts",
                data: [
                    severityCounts.low,
                    severityCounts.medium,
                    severityCounts.high
                ],
                backgroundColor: ["#22c55e", "#f59e0b", "#ef4444"]
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    ticks: { color: "#e2e8f0" }
                },
                y: {
                    ticks: { color: "#e2e8f0" }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#e2e8f0"
                    }
                }
            }
        }
    });
}
