import logging
import os
import sys
import time
from argparse import ArgumentParser
from random import random

from database import SensorData, get_db
from gps import GpsCoordinates, GpsSensor

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

if os.getenv("USE_STUBS", False):
    class GpsSensor:
        # Russia, Moscow
        __lat = 55.751244
        __lon = 37.618423

        @staticmethod
        def get_coordinates():
            time.sleep(0.9 + random() * 0.1)
            GpsSensor.__lat += random() / 500
            GpsSensor.__lon += random() / 500
            logging.debug("GPS generated: %s,%s", GpsSensor.__lat, GpsSensor.__lon)
            return GpsCoordinates(lat=GpsSensor.__lat, lon=GpsSensor.__lon)


def main():
    parser = ArgumentParser()
    parser.add_argument("--db-uri", required=True)
    parser.add_argument("--sensor-id", required=True, type=int)

    args = parser.parse_args()

    gps = GpsSensor()
    logger.info("GPS sensor initialized")

    while True:
        try:
            coordinates = gps.get_coordinates()

            SensorData.save_new(get_db(args.db_uri), args.sensor_id, coordinates)
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
