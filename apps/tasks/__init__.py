# coding: utf-8

from apps.tasks.stock import TaskStockBasic
from apps.tasks.trade_cal import TaskTradeCal
from apps.tasks.namechange import TaskNameChange
from apps.tasks.hs_const import TaskHSConst
from apps.tasks.news import TaskNews


class Task(object):

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

