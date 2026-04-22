import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    
    # Temperature settings
    MIN_TEMP = float(os.environ.get('MIN_TEMP', '76.0'))
    MAX_TEMP = float(os.environ.get('MAX_TEMP', '80.0'))
    
    # Sensor settings
    SENSOR_CHECK_INTERVAL = int(os.environ.get('SENSOR_CHECK_INTERVAL', '300'))  # 5 minutes
    
    # Email alert settings
    # Postmark email settings
    POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY')
    FROM_EMAIL = os.environ.get('FROM_EMAIL', 'alerts@yourdomain.com')
    
    # Logging
    LOG_FILE = 'logs/alerts.log'