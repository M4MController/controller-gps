import logging

import navio2.ublox

logger = logging.getLogger(__name__)


class GpsCoordinates:
    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "{lat},{lon}".format(lat=self.lat, lon=self.lon)

    def is_valid(self):
        return self.lat and self.lon


class GpsSensor:
    def __init__(self):
        self.ubl = ubl = navio2.ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)

        ubl.configure_poll_port()
        ubl.configure_poll(navio2.ublox.CLASS_CFG, navio2.ublox.MSG_CFG_USB)
        # ubl.configure_poll(navio2.ublox.CLASS_MON, navio2.ublox.MSG_MON_HW)

        ubl.configure_port(port=navio2.ublox.PORT_SERIAL1, inMask=1, outMask=0)
        ubl.configure_port(port=navio2.ublox.PORT_USB, inMask=1, outMask=1)
        ubl.configure_port(port=navio2.ublox.PORT_SERIAL2, inMask=1, outMask=0)
        ubl.configure_poll_port()
        ubl.configure_poll_port(navio2.ublox.PORT_SERIAL1)
        ubl.configure_poll_port(navio2.ublox.PORT_SERIAL2)
        ubl.configure_poll_port(navio2.ublox.PORT_USB)
        ubl.configure_solution_rate(rate_ms=1000)

        ubl.set_preferred_dynamic_model(None)
        ubl.set_preferred_usePPP(None)

        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_POSLLH, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_PVT, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_STATUS, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_SOL, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_VELNED, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_SVINFO, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_VELECEF, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_POSECEF, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_RXM, navio2.ublox.MSG_RXM_RAW, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_RXM, navio2.ublox.MSG_RXM_SFRB, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_RXM, navio2.ublox.MSG_RXM_SVSI, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_RXM, navio2.ublox.MSG_RXM_ALM, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_RXM, navio2.ublox.MSG_RXM_EPH, 1)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_TIMEGPS, 5)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_CLOCK, 5)
        ubl.configure_message_rate(navio2.ublox.CLASS_NAV, navio2.ublox.MSG_NAV_DGPS, 5)

    def get_coordinates(self) -> GpsCoordinates:
        while True:
            msg = self.ubl.receive_message()

            if msg is None:
                raise Exception("Can not read NAVIO2 message")
            logger.debug("msg received: %s", msg.name())
            if msg.name() == "NAV_POSLLH":
                msg.unpack()
                if msg.have_field("Latitude") and msg.have_field("Longitude"):
                    lat = msg.Latitude / 10000000
                    lon = msg.Longitude / 10000000
                    logger.debug("GPS received: %s,%s", lat, lon)
                    return GpsCoordinates(lat=lat, lon=lon)
