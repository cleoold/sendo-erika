import logging
import sys

logger = logging.getLogger('sendoerika')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)  # fixme
