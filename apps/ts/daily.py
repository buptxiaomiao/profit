# coding: utf-8

import time
import tushare as ts

from settings.settings import TS_TOKEN
from utils.log_tools import logger
from models.stock import Stock
from models.daily import Daily
from utils.df_to_models import DfToModels


class TsDaily(object):

    ts.set_token(TS_TOKEN)
    pro = ts.pro_api()

    @classmethod
    def run(cls):

        start_date = '20000101'
        mid_date = '20120101'
        end_date = '20191231'
        ma = [2, 5, 10, 12, 26, 30, 60, 120, 250]

        db_res = Stock.query_focus_stocks()
        for i, x in enumerate(db_res):
            try:
                ts_code = x.ts_code

                # 第一部分
                df1 = ts.pro_bar(ts_code=ts_code, pro_api=cls.pro, adj='qfq',
                                 start_date=start_date, end_date=mid_date, ma=ma)
                df1 = df1.fillna(0)
                model_list1 = DfToModels.df2models(df1, Daily, to_dict=True)

                # 第二部分
                df2 = ts.pro_bar(ts_code=ts_code, pro_api=cls.pro, adj='qfq',
                                 start_date=mid_date, end_date=end_date, ma=ma)
                df2 = df2.fillna(0)
                model_list2 = DfToModels.df2models(df2, Daily, to_dict=True)

                Daily.delete_by_ts_code(ts_code=ts_code)
                Daily.batch_insert(model_list1, 1000)
                Daily.batch_insert(model_list2, 1000)
                logger.info('{} -- {} / {}'.format(ts_code, i, len(db_res)))
                time.sleep(0.01)

            except Exception as e:
                logger.error(e.message, exc_info=True)


if __name__ == '__main__':
    TsDaily.run()
