import logging
from prettyprinter import pformat
import threading

logger = logging.getLogger("{{cookiecutter.project_slug}}")


def plog(annotation, args):
    if not args:
        args = []
    log = annotation.lstrip() + ('\n' if args else '')
    for a in args:
        log = log + pformat(a)
    return log


_lock = threading.RLock()


def _acquire_lock():
    """
    Acquire the module-level lock for serializing access to shared data.

    This should be released with _releaseLock().
    """
    if _lock:
        _lock.acquire()


def _release_lock():
    """
    Release the module-level lock acquired by calling _acquireLock().
    """
    if _lock:
        _lock.release()


def get_logger(name):
    if not isinstance(name, str):
        raise TypeError('A logger name must be a string')
    name = name.lstrip()
    _acquire_lock()
    try:
        logger = plogger_manager.get_logger(name)
        if not logger:
            logger = plogger(name)
            plogger_manager.set_logger(name, logger)
    finally:
        _release_lock()
    return logger


class plogger(object):

    def __init__(self, cls_name: str):
        self.cls_name = cls_name.lstrip()

    def __get_plog(self, annotation: str, args):
        return self.cls_name + ": " + plog(annotation, args)

    def debug(self, annotation: str, *args):
        logger.debug(self.__get_plog(annotation, args))

    def info(self, annotation: str, *args):
        logger.info(self.__get_plog(annotation, args))

    def warning(self, annotation: str, *args):
        logger.warning(self.__get_plog(annotation, args))

    def error(self, annotation: str, *args):
        logger.info(self.__get_plog(annotation, args))

    def critical(self, annotation: str, *args):
        logger.critical(self.__get_plog(annotation, args))

    def exception(self, annotation: str, *args):
        logger.exception(annotation)


class plogger_manager(object):
    logger_dict = dict()

    @classmethod
    def set_logger(cls, name, logger):
        cls.logger_dict[name] = logger

    @classmethod
    def get_logger(cls, name):
        return cls.logger_dict.get(name)
