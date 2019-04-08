# coding: utf-8

from models.trade_cal import TradeCal
from models.stock import Stock


def func():
    """
    20000101 - 2019年12月31号，日线的总数据量
    :return:
    """
    db_res = TradeCal.select(TradeCal.cal_date).where(TradeCal.is_open == 1).order_by(TradeCal.cal_date)
    l = len(db_res)
    d = dict()
    for i, x in enumerate(db_res):
        the_day = int(x.cal_date)
        d[the_day] = i + 1

    end = d[20191231]
    result = []
    # db_res = Stock.select(Stock.list_date).where(Stock.list_status == 'L')
    db_res = Stock.query_focus_stocks()
    for x in db_res:
        the_day = int(x.list_date)
        if the_day <= 20000104:
            the_day = 20000104
        # if the_day <= 20140102:
        #     the_day = 20140102

        start = d[the_day]
        result.append(end - start)

    print sum(result)


if __name__ == '__main__':
    func()
