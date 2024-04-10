import logging
import logging.config

from yatg.settings import Settings


def build_logger():
    settings = Settings()
    logger = logging.getLogger('yatg')
    logging.config.dictConfig(settings.logger_config)
