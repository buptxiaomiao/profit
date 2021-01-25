# coding: utf-8

from apps.ts_task.stock import TaskStockBasic
from apps.ts_task.trade_cal import TaskTradeCal
from apps.ts_task.namechange import TaskNameChange
from apps.ts_task.hs_const import TaskHSConst
from apps.ts_task.news import TaskNews
from apps.ts_task.daily import TaskDaily
from apps.ts_task.stock_company import TaskStockCompany
from apps.ts_task.moneyflow_hsgt import TaskMoneyFlowHsgt
from apps.ts_task.fund.fund_basic import TaskFundBasic
from apps.ts_task.fund.fund_portfolio import TaskFundPortfolio


class TsTask(object):

    @classmethod
    def fund(cls):
        """获取基金相关数据"""
        from apps.ts_task.fund import Fund
        return Fund

    @classmethod
    def stock(cls):
        """获取股票相关数据"""
        from apps.ts_task.stock import Stock
        return Stock

    @classmethod
    def stock_company(cls):
        return TaskStockCompany.run

    @classmethod
    def trade_cal(cls):
        return TaskTradeCal.run

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
        return TaskDaily.run

    @classmethod
    def moneyflow_hsgt(cls):
        return TaskMoneyFlowHsgt.run
