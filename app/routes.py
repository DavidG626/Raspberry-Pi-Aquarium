from flask import Blueprint, render_template, jsonify
from datetime import datetime
import os

# Create blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    # Main dashboard page showing current tank status
    from app import get_monitor
    monitor = get_monitor()
    
    if monitor:
        temp = monitor.current_temp
        last_check = monitor.last_check
        alerts_today = monitor.alerts_today
    else:
        temp = None
        last_check = None
        alerts_today = 0
    
    return render_template('dashboard.html', 
                         temp=temp,
                         last_check=last_check,
                         alerts_today=alerts_today)

@main.route('/api/temperature')
def get_temperature():
    # API endpoint for current temperature data
    from app import get_monitor
    monitor = get_monitor()
    
    if monitor:
        temp = monitor.current_temp
        last_check = monitor.last_check
        alerts_today = monitor.alerts_today
        
        # Check if temperature is in safe range
        status = 'good'
        if temp and (temp < 76.0 or temp > 80.0):
            status = 'alert'
            
    else:
        temp = None
        last_check = None
        alerts_today = 0
        status = 'unknown'
    
    return jsonify({
        'temperature': temp,
        'last_check': last_check.isoformat() if last_check else None,
        'alerts_today': alerts_today,
        'status': status
    })

@main.route('/logs')
def view_logs():
    # Simple page to view recent alert logs
    log_file = 'logs/alerts.log'
    logs = []
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = f.readlines()[-20:]  # Last 20 log entries
    
    return render_template('logs.html', logs=logs)