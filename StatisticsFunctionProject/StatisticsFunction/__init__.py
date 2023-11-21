import logging
import json

def main(sensorDataChanges) -> None:
    # see the database change
    logging.info("SQL Changes: %s\n", json.loads(sensorDataChanges))
    # read already existing data from the database