import logging
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    create_engine,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from gps import GpsCoordinates

logger = logging.getLogger(__name__)

Base = declarative_base()

session = None


def get_db(db_uri):
    global session
    if session is not None:
        return session

    session = Session(create_engine(db_uri))

    return session


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)

    sensor_id = Column(Integer, nullable=False)

    @staticmethod
    def save_new(session, sensor_id, coordinates: GpsCoordinates):
        now = datetime.now()
        data = {
            'timestamp': now.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            'value': {'lat': coordinates.lat, 'lon': coordinates.lon},
        }
        s = SensorData(data=data, sensor_id=sensor_id)
        session.add(s)
        session.commit()

        logger.info("Data saved to DB: data=%s sensor_id=%s", data, sensor_id)

        return s
