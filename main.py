import logging
import os
import uuid

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


def get_sensor_uuid():
    if not os.path.exists('uuid'):
        sensor_uuid = uuid.uuid4().hex
        with open('uuid', 'w+') as f:
            f.write(sensor_uuid)
    else:
        with open('uuid', 'r') as f:
            sensor_uuid = f.readline()
    return sensor_uuid


def init_sensor(uri, sensor_uuid):
    while not (200 <= requests.post(
            '{uri}/private/sensor/{sensor_uuid}/register'.format(uri=uri, sensor_uuid=sensor_uuid),
            json={'sensor_type': 6, 'status': 1},
    ).status_code < 300):
        pass


def send_coordinates(uri, sensor_uuid, coordinates):
    requests.post(
        '{uri}/private/sensor/{sensor_uuid}/data'.format(uri=uri, sensor_uuid=sensor_uuid),
        json={'value': {'lat': coordinates.lat, 'lon': coordinates.lon}},
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("--uri", required=True)

    args = parser.parse_args()

    sensor_uuid = get_sensor_uuid()
    init_sensor(args.uri, sensor_uuid)

    gps = GpsSensor()
    logger.info("GPS sensor initialized")

    while True:
        try:
            send_coordinates(args.uri, sensor_uuid, gps.get_coordinates())
        except Exception as e:
            logging.error(e)


if __name__ == "__main__":
    main()
