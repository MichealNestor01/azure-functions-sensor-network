from typing import Any
from sensor import Sensor
import requests
from datetime import datetime, timedelta
import time

URL = "https://distributed-systems-coursework-data-function.azurewebsites.net/api/datafunction"
TOTAL_SENSORS = 20
# start time is 9am on 15/11/2023, sensors produce data once an hour
# sensors were active for 10 hours
START_TIME = datetime(2023, 11, 16, 10)
INTERVAL = timedelta(minutes=60)
TOTAL_HOURS = 1

def report_to_data_function(sensor: Sensor, timestamp: datetime) -> None:
    print(f"Sending data from sensor {sensor.id} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')} to DataFunction")
    sensor_values: dict[str, Any] = sensor.get_sensor_values_as_dict()
    sensor_values["id"] = sensor.id
    sensor_values["timestamp"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    res = requests.post(URL, json=sensor_values)
    print(f"Response ({res.status_code}): {res.text}")

def main() -> None:
    # create the array of sensors
    sensor_array = [Sensor(i) for i in range(TOTAL_SENSORS)]
    # report data from each sensor and update it
    print("Sensor Network Starting")
    current_time = START_TIME
    for _ in range(TOTAL_HOURS):
        for sensor in sensor_array:
            report_to_data_function(sensor, current_time)
            sensor.update()
        current_time += INTERVAL

if __name__ == "__main__":
    main()
