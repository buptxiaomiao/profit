# coding: utf-8

from peewee import IntegerField, DateTimeField, CharField, SmallIntegerField, fn
from utils.db_tools import BaseModel


class TradeCal(BaseModel):

    class Meta:
        db_table = 'trade_cal'

    id = IntegerField(primary_key=True)
    exchange = CharField(8, default='')        # 交易所代码, SSE上交所 SZSE深交所
    cal_date = CharField(16, default='')        # 日历日期, '20191231'
    is_open = SmallIntegerField(1, default=0)   # 是否交易 0休市 1交易
    pretrade_date = CharField(16, default='')   # 上一个交易日
    create_time = DateTimeField()
    update_time = DateTimeField()
