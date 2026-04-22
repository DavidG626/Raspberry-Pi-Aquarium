import time
import logging
import requests
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sensor.interface import AquariumSensor

# Set up dedicated logger for temperature alerts only
alert_logger = logging.getLogger('temperature_alerts')
alert_logger.setLevel(logging.WARNING)

# Create file handler specifically for alerts
alert_handler = logging.FileHandler('logs/alerts.log')
alert_handler.setLevel(logging.WARNING)
alert_formatter = logging.Formatter('%(asctime)s - %(message)s')
alert_handler.setFormatter(alert_formatter)

# Add handler to our specific logger
alert_logger.addHandler(alert_handler)

# Prevent this logger from sending messages to root logger (avoids Flask logs)
alert_logger.propagate = False


class TemperatureMonitor:
    def __init__(self, config):
        self.config = config
        self.sensor = AquariumSensor()
        self.scheduler = BackgroundScheduler()
        
        # Current readings (shared with Flask routes)
        self.current_temp = None
        self.last_check = None
        self.alerts_today = 0
        
    def check_temperature(self):
        # Read current temperature from sensor
        try:
            temp = self.sensor.read_temperature()
            
            if temp is None:
                print("Could not read sensor")
                return
                
            # Update current readings
            self.current_temp = temp
            self.last_check = datetime.now()
            
            # Check if temperature is in safe range
            if temp < self.config.MIN_TEMP:
                self.send_alert(f"COLD ALERT: Tank temperature {temp}°F is below safe minimum {self.config.MIN_TEMP}°F")
                
            elif temp > self.config.MAX_TEMP:
                self.send_alert(f"HOT ALERT: Tank temperature {temp}°F is above safe maximum {self.config.MAX_TEMP}°F")
                
            else:
                print(f"Temperature OK: {temp}°F")
                
        except Exception as e:
            print(f"Error during temperature check: {e}")
            
    def send_alert(self, message):
        # Send email alert via Postmark and log it
        try:
            # Send via Postmark API
            response = requests.post(
                "https://api.postmarkapp.com/email",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "X-Postmark-Server-Token": self.config.POSTMARK_API_KEY
                },
                json={
                    "From": self.config.FROM_EMAIL,
                    "To": self.config.ALERT_EMAIL,
                    "Subject": "Aquarium Temperature Alert",
                    "TextBody": f"""Aquarium Alert!

{message}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Check your tank immediately."""
                }
            )
            
            if response.status_code == 200:
                # Log the alert
                alert_logger.warning(message)
                self.alerts_today += 1
                print(f"Alert sent via Postmark: {message}")
            else:
                print(f"Postmark failed: {response.text}")
                
        except Exception as e:
            print(f"Failed to send alert: {e}")
            # Still log the alert even if email fails
            alert_logger.warning(message)
            self.alerts_today += 1
            
    def start_monitoring(self):
        # Start background temperature checking
        self.scheduler.add_job(
            func=self.check_temperature,
            trigger="interval",
            seconds=self.config.SENSOR_CHECK_INTERVAL,
            id='temp_check'
        )
        
        self.scheduler.start()
        print("Temperature monitoring started")
        
        # Do initial check right away
        self.check_temperature()