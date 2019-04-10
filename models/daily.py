# coding: utf-8

from peewee import IntegerField, DateTimeField, CharField, FloatField, fn
from utils.db_tools import BaseModel


class Daily(BaseModel):

    class Meta:
        db_table = 'daily'

    id = IntegerField(primary_key=True)
    ts_code = CharField(32, default='')         # TS代码
    trade_date = IntegerField(11, default=0)    # 交易日期
    open = FloatField(default=0)        # 开盘价
    high = FloatField(default=0)        # 最高价
    low = FloatField(default=0)         # 最低价
    close = FloatField(default=0)       # 收盘价
    pre_close = FloatField(default=0)   # 昨收价
    change = FloatField(default=0)      # 涨跌额
    pct_chg = FloatField(default=0)     # 涨跌幅
    vol = FloatField(default=0)         # 成交量（手）
    amount = FloatField(default=0)      # 成交额 （千元）
    ma2 = FloatField(default=0)    # 2日均价
    ma5 = FloatField(default=0)    # 5日均价
    ma10 = FloatField(default=0)   # 10日均价
    ma12 = FloatField(default=0)   # 12日均价
    ma26 = FloatField(default=0)   # 26日均价
    ma30 = FloatField(default=0)   # 30日均价
    ma60 = FloatField(default=0)   # 60日均价
    ma120 = FloatField(default=0)  # 120日均价
    ma250 = FloatField(default=0)  # 250日均价
    ma_v_2 = FloatField(default=0)      # 2日均成交量（手）
    ma_v_5 = FloatField(default=0)      # 5日均成交量（手）
    ma_v_10 = FloatField(default=0)     # 10日均成交量（手）
    ma_v_12 = FloatField(default=0)     # 12日均成交量（手）
    ma_v_26 = FloatField(default=0)     # 26日均成交量（手）
    ma_v_30 = FloatField(default=0)     # 30日均成交量（手）
    ma_v_60 = FloatField(default=0)     # 60日均成交量（手）
    ma_v_120 = FloatField(default=0)    # 120日均成交量（手）
    ma_v_250 = FloatField(default=0)    # 250日均成交量（手）
    create_time = DateTimeField()
    update_time = DateTimeField()

    @classmethod
    def delete_by_ts_code(cls, ts_code):
        db_res = cls.select().where(cls.ts_code == ts_code).limit(1)
        if db_res:
            return cls.delete().where(cls.ts_code == ts_code).execute()
        return None
