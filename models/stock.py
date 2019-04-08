# coding: utf-8

from peewee import IntegerField, DateTimeField, CharField, fn
from utils.db_tools import BaseModel


class Stock(BaseModel):

    class Meta:
        db_table = 'stock'

    id = IntegerField(primary_key=True)
    ts_code = CharField(32, default='')         # TS代码
    symbol = CharField(32, default='')          # 股票代码
    name = CharField(128, default='')           # 股票名称
    area = CharField(16, default='')            # 所在地域
    industry = CharField(32, default='')        # 所属行业
    market = CharField(32, default='')          # 主板/中小板/创业板
    exchange = CharField(32, default='')        # 交易所代码, SSE上交所 SZSE深交所
    list_status = CharField(8, default='')      # L上市 D退市 P暂停上市
    list_date = CharField(32, default='')       # 上市时间
    is_hs = CharField(32, default='')           # 是否沪深港通标的，N否 H沪股通 S深股通
    create_time = DateTimeField()
    update_time = DateTimeField()

    @classmethod
    def query_focus_stocks(cls):
        """
        正在上市、非创业板、非ST
        :return:
        """
        db_res = cls.select().where(cls.list_status == 'L', cls.market != '创业板').order_by(cls.ts_code)

        result = []
        for x in db_res:
            if 'ST' in x.name:
                continue
            result.append(x)
        return result
