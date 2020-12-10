from logging import getLogger
from logging import StreamHandler
from logging import FileHandler
from logging import Formatter
from logging import NOTSET
from logging import DEBUG
from logging import INFO
from logging import WARNING
from logging import ERROR
from logging import CRITICAL
from colorlog import ColoredFormatter
from pathlib import Path

log = getLogger(__name__)

# # Sample codes. (Write at the top of main().)
# ao.setup_simple_logger()
# ao.setup_simple_logger(outputfile="tmp.log")
# ao.setup_detail_logger()
# ao.setup_detail_logger(outputfile="tmp.log")

def _lookup_level(key):
    d = {
        "NOTSET": NOTSET,
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
    }
    return d.get(key, NOTSET)

def _setup_logger(logger, format, outputfile, level):
    sh = StreamHandler()
    formatter = ColoredFormatter('%(log_color)s' + format)
    formatter.log_colors["DEBUG"] = "blue"
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    if outputfile is not None:
        outpath = Path(outputfile)
        fh = FileHandler(outpath, encoding='utf-8')
        formatter = Formatter(format)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    logger.setLevel(level)
    sh.setLevel(level)
    return logger

def setup_detail_logger(outputfile=None, level=DEBUG):
    if isinstance(level, str):
        level = _lookup_level(level)
    root_logger = getLogger()
    format = '%(asctime)s [%(levelname)s] %(name)s > %(message)s'
    return _setup_logger(root_logger, format, outputfile, level)

def setup_simple_logger(outputfile=None, level=NOTSET):
    if isinstance(level, str):
        level = _lookup_level(level)
    root_logger = getLogger()
    format = '[%(levelname)s] %(message)s'
    return _setup_logger(root_logger, format, outputfile, level)

def test_log():
    log.debug("debug.")
    log.info("info.")
    log.warn("warning.")
    log.error("error.")
    log.critical("critical.")
