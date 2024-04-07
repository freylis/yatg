import logging


def build_logger():
    lg = logging.Logger('yatg')
    lg.setLevel('DEBUG')
    lg.addHandler(logging.StreamHandler())
    return lg


logger = build_logger()
