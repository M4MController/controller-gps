import logging
import os
import requests
import sys
import time
from argparse import ArgumentParser
from random import random

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
            GpsSensor.__lat += (random() - 0.5) / 10000
            GpsSensor.__lon += (random() - 0.5) / 10000
            logging.debug("GPS generated: %s,%s", GpsSensor.__lat, GpsSensor.__lon)
            return GpsCoordinates(lat=GpsSensor.__lat, lon=GpsSensor.__lon)


def main():
    parser = ArgumentParser()
    parser.add_argument("--uri", required=True)
    parser.add_argument("--sensor-id", required=True, type=int)

    args = parser.parse_args()

    gps = GpsSensor()
    logger.info("GPS sensor initialized")

    while True:
        try:
            coordinates = gps.get_coordinates()

            requests.post(
                '{uri}/private/sensor/{sensor_id}/data'.format(uri=args.uri, sensor_id=args.sensor_id),
                json={'value': {'lat': coordinates.lat, 'lon': coordinates.lon}},
            )
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
