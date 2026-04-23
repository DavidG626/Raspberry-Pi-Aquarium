# Aquarium Temperature Monitor

Real-time temperature monitoring system for my 55-gallon aquarium using Raspberry Pi and DS18B20 sensor.

## Features

- **24/7 Monitoring**: Checks temperature every 5 minutes
- **Email Alerts**: Instant notifications when temperature goes outside safe range (76-80°F)
- **Web Dashboard**: Real-time status with dark/light mode toggle
- **Alert Logging**: Historical alert tracking
- **REST API**: JSON endpoint for external integrations

## Hardware

- Raspberry Pi (any model with GPIO)
- DS18B20 Waterproof Temperature Sensor
- 4.7kΩ resistor (pull-up for DS18B20)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aquarium-monitor.git
cd aquarium-monitor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
python app.py
```

5. Access dashboard at `http://localhost:5004`

## Configuration

- **Temperature Range**: 76.0°F - 80.0°F (configurable)
- **Check Interval**: 5 minutes (configurable)
- **Email Alerts**: Via Postmark API

## API Endpoints

- `GET /` - Main dashboard
- `GET /api/temperature` - Current temperature data (JSON)
- `GET /logs` - Alert history

## Deployment

Designed for Raspberry Pi deployment with systemd service for automatic startup.

## License

MIT License
