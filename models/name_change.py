# coding: utf-8

from peewee import IntegerField, DateTimeField, CharField, fn
from utils.db_tools import BaseModel


class NameChange(BaseModel):

    class Meta:
        db_table = 'namechange'

    id = IntegerField(primary_key=True)
    ts_code = CharField(16, default='')         # TS代码
    name = CharField(128, default='')           # 证券名称
    start_date = CharField(16, default='')      # 开始日期
    end_date = CharField(16, default='')        # 结束日期
    change_reason = CharField(128, default='')  # 变更原因
    ann_date = CharField(16, default=0)         # 公告日期
    create_time = DateTimeField()
    update_time = DateTimeField()