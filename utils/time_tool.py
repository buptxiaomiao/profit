# coding: utf-8

import time
import datetime
import logging
from dateutil import parser

logger = logging.getLogger(__name__)


class TimeTool(object):
    """时间处理工具类"""

    timedelta = datetime.timedelta
    datetime = datetime.datetime

    @classmethod
    def timestamp2datetime(cls, _timestamp):
        if isinstance(_timestamp, datetime.datetime):
            return _timestamp
        return datetime.datetime.fromtimestamp(int(_timestamp))

    @classmethod
    def datetime2timestamp(cls, _datetime):
        if not _datetime:
            return 0
        if isinstance(_datetime, float) or isinstance(_datetime, int):
            return int(_datetime)
        return int(time.mktime(cls.str_to_datetime(_datetime).timetuple()))

    @classmethod
    def now_timestamp_int(cls):
        return int(time.time())

    @classmethod
    def now_timestamp(cls):
        return time.time()

    @classmethod
    def now(cls, days=0):
        """days 为0时，返回当前时间，为其他整数时，返回当前时间前几天或后几天的时间"""
        d = datetime.datetime.now()
        if not isinstance(days, int):  # days不是整数时直接返回当前时间
            return d
        return d + datetime.timedelta(days=days) if days else d

    @classmethod
    def now_date(cls, days=0):
        """days 为0时，返回当前时间，为其他整数时，返回当前时间前几天或后几天的日期"""
        d = datetime.date.today()
        if not isinstance(days, int):
            return d
        return d + datetime.timedelta(days=days) if days else d

    @classmethod
    def date_to_datetime(cls, d):
        if type(d) == datetime.date:
            return datetime.datetime(year=d.year, month=d.month, day=d.day)
        return d

    @classmethod
    def datetime_to_date(cls, d):
        if type(d) == datetime.datetime:
            return datetime.date(year=d.year, month=d.month, day=d.day)
        return d

    @classmethod
    def get_datetime_pair(cls, dt):
        """获取当天日期的起止时间"""
        start_time = cls.datetime_to_date(dt) or datetime.date.today()
        end_time = start_time + datetime.timedelta(days=1)
        return start_time, end_time

    @classmethod
    def get_timestamp_pair(cls, dt):
        """获取昨天起止时间戳"""
        start_time = cls.datetime_to_date(dt) or datetime.date.today()
        end_time = start_time + datetime.timedelta(days=1)
        start_ts = int(time.mktime(start_time.timetuple()))
        end_ts = int(time.mktime(end_time.timetuple()))
        return start_ts, end_ts

    @classmethod
    def datetime_to_str(cls, d, fmt='%Y-%m-%d %H:%M:%S'):
        """将 datetime 类型, 格式化为字符串, 格式化失败时返回 ''"""
        if not d:
            return ''
        if isinstance(d, str):
            return d
        if isinstance(d, unicode):
            return cls.s(d)
        return cls.date_to_datetime(d).strftime(fmt)

    @classmethod
    def str_to_datetime(cls, s):
        """将日期字符串转换为 datetime 类型, 转换失败返回 None"""
        if isinstance(s, datetime.date):
            return cls.date_to_datetime(s)
        if isinstance(s, datetime.datetime):
            return s
        # unicode转str
        s = cls.s(s)
        if not isinstance(s, str) or not s:
            return None
        try:
            return parser.parse(s)
        except Exception, e:
            logger.error('TimeTool str_to_datetime error %s, [%s]' % (e, s))
            return None

    @classmethod
    def s(cls, u, strip=True, charset='utf-8', default=''):
        """将unicode转换为str"""
        if not isinstance(u, (str, unicode)):
            return default
        if isinstance(u, unicode):
            u = u.encode(charset)
        return u.strip() if strip else u
