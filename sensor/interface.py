import time

class AquariumSensor:
    # Temperature sensor monitoring my 55 gallon tank
    
    def __init__(self):
        # Sensor ID from my raspberry pi setup
        self.sensor_id = '28-011432e42eff'
        self.sensor_file = f'/sys/bus/w1/devices/{self.sensor_id}/w1_slave'
        
    def read_temperature(self):
        # Read current temperature 
        try:
            with open(self.sensor_file, 'r') as f:
                lines = f.readlines()
                
            # Make sure sensor reading is valid
            if lines[0].strip()[-3:] != 'YES':
                print("Sensor reading invalid, retrying...")
                time.sleep(0.2)
                return self.read_temperature()
                
            # Parse temperature data
            temp_line = lines[1]
            temp_data = temp_line.split('t=')[1]
            temp_celsius = float(temp_data) / 1000.0
            temp_fahrenheit = (temp_celsius * 9/5) + 32
            
            return round(temp_fahrenheit, 1)
            
        except FileNotFoundError:
            print("Sensor not found - check wiring")
            return None
        except Exception as e:
            print(f"Error reading sensor: {e}")
            return None