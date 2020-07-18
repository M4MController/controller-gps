import logging
import random
import uuid

logger = logging.getLogger(__name__)


def get_hardware_id() -> str:
	# extract serial from cpuinfo file
	result = None
	try:
		f = open('/proc/cpuinfo', 'r')
		for line in f:
			if line[0:6] == 'Serial':
				result = line[10:26]
				break
		f.close()
	except Exception as e:
		logger.exception(e)

	if not result:
		logger.error("Can not get hardware id (result = %s)", result)
		result = str(uuid.getnode())

	return result


def get_rand_bits(s: str) -> int:
	a = random.Random(s)
	return a.getrandbits()


def generate_uuid():
	rand = random.Random(f"{get_hardware_id()}_gps")

	return uuid.UUID(int=rand.getrandbits(128)).hex
