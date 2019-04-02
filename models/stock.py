# coding: utf-8

from peewee import IntegerField, DateTimeField, CharField, fn
from utils.db_tools import BaseModel


class Stock(BaseModel):

    class Meta:
        db_table = 'stock'

    id = IntegerField(primary_key=True)
    ts_code = CharField(32)         # TS代码
    symbol = CharField(32)          # 股票代码
    name = CharField(128)           # 股票名称
    area = CharField(16)            # 所在地域
    industry = CharField(32)        # 所属行业
    market = CharField(32)          # 主板/中小板/创业板
    exchange = CharField(32)        # 交易所代码
    list_status = CharField(8)      # L上市 D退市 P暂停上市
    list_date = CharField(32)       # 上市时间
    is_hs = CharField(32)           # 是否沪深港通标的，N否 H沪股通 S深股通
    create_time = DateTimeField()
    update_time = DateTimeField()
