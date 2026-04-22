from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize temperature monitor
    from app.monitor import TemperatureMonitor
    monitor = TemperatureMonitor(Config)
    
    # Set the global monitor so routes can access it
    from app import set_monitor
    set_monitor(monitor)
    
    # Register blueprints (routes)
    from app.routes import main
    app.register_blueprint(main)
    
    # Start background monitoring
    monitor.start_monitoring()
    
    return app

if __name__ == '__main__':
    app = create_app()
    try:
        app.run(debug=True, host='0.0.0.0', port=5004)
    except KeyboardInterrupt:
        print("\nShutting down temperature monitoring...")
        from app import get_monitor
        monitor = get_monitor()
        if monitor:
            monitor.scheduler.shutdown()