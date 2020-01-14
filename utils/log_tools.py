# coding: utf-8

import os
import fcntl
import time
import logging
from logging.handlers import TimedRotatingFileHandler
# from raven.conf import setup_logging
#
# from util.sentry_client import handler


class LevelFilter(logging.Filter):
    """
    http://stackoverflow.com/a/7447596/190597 (robert)
    """
    def __init__(self, level):
        super(LevelFilter, self).__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


class MultiCompatibleTimedRotatingFileHandler(TimedRotatingFileHandler):

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        # 兼容多进程并发 LOG_ROTATE
        if not os.path.exists(dfn):
            with open(self.baseFilename, 'a') as f:
                fcntl.lockf(f.fileno(), fcntl.LOCK_EX)
                if not os.path.exists(dfn):
                    os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not getattr(self, 'delay', False):
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


def gen_handler(log_path, error=False):
    log_path = log_path
    str_format = "%(asctime)s: %(name)s:%(levelname)s:%(message)s"
    date_fmt = "%Y-%m-%dT%H:%M:%S"

    if error:
        name = "{0}error.log".format(log_path)
        handler = MultiCompatibleTimedRotatingFileHandler(filename=name, when='MIDNIGHT')
        handler.setLevel(level=logging.ERROR)
        handler.addFilter(LevelFilter(logging.ERROR))
    else:
        name = "{0}info.log".format(log_path)
        handler = MultiCompatibleTimedRotatingFileHandler(filename=name, when='MIDNIGHT')
        handler.setLevel(level=logging.INFO)
        handler.addFilter(LevelFilter(logging.INFO))

    formatter = logging.Formatter(str_format, date_fmt)
    handler.setFormatter(formatter)

    return handler


class BaseLogger(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.level = logging.INFO

    def gen_logger(self, log_path):
        # set produce log level
        self.logger.setLevel(self.level)

        # gen two handler and set it on the logger
        handler_info = gen_handler(log_path)
        handler_error = gen_handler(log_path, error=True)
        self.logger.addHandler(handler_info)
        self.logger.addHandler(handler_error)
        # # inti sentry
        # handler.setLevel(logging.ERROR)
        # setup_logging(handler)

        return self.logger


def _get_log_path(dir_name):
    log_path = '{}/{}/'.format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dir_name)
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    return log_path


logger = BaseLogger('logger').gen_logger(_get_log_path('log'))
