# coding: utf-8


class Stock(object):

    @classmethod
    def daily_basic(cls):
        """沪深股票 每日指标"""
        from apps.ts_task.stock.daily_basic import TaskDailyBasic
        return TaskDailyBasic
