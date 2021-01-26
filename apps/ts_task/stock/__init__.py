# coding: utf-8


class Stock(object):

    @classmethod
    def daily_basic(cls):
        """沪深股票 每日指标"""
        from apps.ts_task.stock.daily_basic import TaskDailyBasic
        return TaskDailyBasic

    @classmethod
    def stock_basic(cls):
        from apps.ts_task.stock.stock_basic import TaskStockBasic
        return TaskStockBasic
