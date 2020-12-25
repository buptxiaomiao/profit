# coding: utf-8


class Fund(object):

    @classmethod
    def fund_basic(cls):
        """基金基础信息"""
        from apps.ts_task.fund.fund_basic import TaskFundBasic
        return TaskFundBasic.run

    @classmethod
    def fund_portfolio(cls):
        """基金持仓公告"""
        from apps.ts_task.fund.fund_portfolio import TaskFundPortfolio
        return TaskFundPortfolio.run

