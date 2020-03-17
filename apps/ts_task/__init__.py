# coding: utf-8

from apps.ts_task.stock import TaskStockBasic
from apps.ts_task.trade_cal import TaskTradeCal
from apps.ts_task.namechange import TaskNameChange
from apps.ts_task.hs_const import TaskHSConst
from apps.ts_task.news import TaskNews
from apps.ts_task.daily import TaskDaily


class TsTask(object):

    @classmethod
    def stock(cls):
        return TaskStockBasic.run()

    @classmethod
    def trade_cal(cls):
        return TaskTradeCal.run()

    @classmethod
    def namechange(cls):
        return TaskNameChange.run()

    @classmethod
    def hs_const(cls):
        return TaskHSConst.run()

    @classmethod
    def news(cls):
        return TaskNews.run()

    @classmethod
    def daily(cls):
        return TaskDaily.run()
