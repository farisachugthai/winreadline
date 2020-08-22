

def init_logger(log_level: int = logging.DEBUG, propagate: bool = False, fmt_msg: str = None, date_fmt: str = None) -> object:
    """Returns the pyreadline_logger used throughout the rest of the repo.

    Parameters
    ----------

    Returns
    -------
    `logging.Logger`.

    """
    logger = logging.getLogger("PYREADLINE")
    logger.setLevel(log_level)
    logger.propagate = propagate
    if fmt_msg is None:
        fmt_msg = "%(message)s"
    if date_fmt is None:
        datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt_msg, datefmt)
    handler = logging.StreamHandler()
    handler.setLevel(level=log_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addFilter(logging.Filter())

    return logger


