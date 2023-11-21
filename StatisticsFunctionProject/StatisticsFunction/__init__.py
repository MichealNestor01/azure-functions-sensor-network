import azure.functions as func
import logging
import json

def main(sensorDataChanges: str, sensorData: func.SqlRowList) -> None:
    change_operations = json.loads(sensorDataChanges)
    logging.info("SQL Changes: %s\n", change_operations)
    # read historical data from the database
    rows = list(map(lambda r: json.loads(r.to_json()), sensorData))

    # organise the newly changed data by sensor
    # could use this code if you decided to setup warnings about irregular new values
    # for example "warning temperature reported is two stdvs above the mean" however 
    # this is outside the scope of this coursework :(
    #sensors_that_changed: dict[str, dict[str, str or int]] = {} 
    #for operation in change_operations: 
    #    if operation['Item']['id'] not in sensors_that_changed:
    #        sensors_that_changed[operation['Item']['id']] = operation['Item']

    # organise historical data by sensor
    sensors: dict[str, list[dict[str, str or int]]] = {}
    for row in rows:
        if row['id'] not in sensors:
            sensors[row['id']] = [row]
        else:
            sensors[row['id']].append(row)
    
    # create 1 log message, that is complient with the json specification
    log_messages = ["["]
    
    # for each sensor gather statistics
    for sensor in sensors.keys():
        # for each sensor attriubte we have [min_val, mean_val, max_val]
        min_avg_max_temp_wind_humid_CO2 = [
            ["temp", 15, 0, 8], 
            ["wind", 25, 0, 15], 
            ["humid", 70, 0, 40], 
            ["CO2", 1500, 0, 500]
        ]
        for data_point in sensors[sensor]:
            # adjust each metric
            for metric in min_avg_max_temp_wind_humid_CO2:
                val = data_point[metric[0]]
                # adjust min
                if val < metric[1]:
                    metric[1] = val
                # adjust max
                elif val > metric[1]:
                    metric[3] = val
                metric[2] += val
        # generate log message, and update mean
        log_message = [f"\"sensor_{sensor}_stats:\" {{ "]
        for metric in min_avg_max_temp_wind_humid_CO2:
            metric[2] /= len(sensors[sensor])
            log_message.append(
                f"\"{metric[0]}\": {{\"min\": {metric[1]}, \"mean\": {round(metric[2], 2)}, \"max\": {metric[3]}}}, "
            )
        log_message[-1] = log_message[-1][:-2]
        log_message.append("},")
        log_messages.append("".join(log_message))
    # adjust formatting of last entry to compy with json spec
    new_end = list(log_messages[-1])
    new_end[-1] = "]"
    log_messages[-1] = "".join(new_end)
    # log sensor metrics
    logging.info("".join(log_messages))