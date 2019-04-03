# coding: utf-8

from peewee import IntegerField, DateTimeField, CharField, SmallIntegerField, fn
from utils.db_tools import BaseModel


class HSConst(BaseModel):

    class Meta:
        db_table = 'hs_const'

    id = IntegerField(primary_key=True)
    ts_code = CharField(16, default='')         # TS代码
    hs_type = CharField(8, default='')          # 沪深港通类型SH沪SZ深
    in_date = CharField(16, default='')         # 纳入日期
    out_date = CharField(16, default='')        # 剔除日期
    is_new = SmallIntegerField(1, default=0)    # 是否最新 1是 0否
    create_time = DateTimeField()
    update_time = DateTimeField()
