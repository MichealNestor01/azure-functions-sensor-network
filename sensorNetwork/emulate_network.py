from sensor import Sensor
import requests

URL = "http://localhost:7071/api/DataFunction"
TOTAL_SENSORS = 20

def report_to_data_function(sensor: Sensor) -> None:
    print(f"Sending data from sensor {sensor.id} to DataFunction")
    sensor_values = sensor.get_sensor_values_as_dict()
    sensor_values["id"] = sensor.id
    res = requests.post(URL, json=sensor_values)
    print(f"Response ({res.status_code}): '{res.text}'")

def main() -> None:
    # create the array of sensors
    sensor_array = [Sensor(i) for i in range(TOTAL_SENSORS)]
    # report data from each sensor and update it
    print("Sensor Network Starting")
    for _ in range(10):
        for sensor in sensor_array:
            report_to_data_function(sensor)
            sensor.update()

if __name__ == "__main__":
    main()
