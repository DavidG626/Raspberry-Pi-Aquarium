# Global monitor instance so routes can access current data
monitor = None

def get_monitor():
    # Helper function for routes to access monitor data
    return monitor

def set_monitor(monitor_instance):
    # Helper function to set the monitor instance
    global monitor
    monitor = monitor_instance