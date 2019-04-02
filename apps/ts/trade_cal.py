# coding: utf-8

import tushare as ts
from settings.settings import TS_TOKEN
from models.trade_cal import TradeCal
from utils.df_to_models import DfToModels


class TsTradeCal(object):

    @classmethod
    def run(cls):
        """
        交易日历
        https://tushare.pro/document/2?doc_id=26
        :return:
        """
        # 设置ts token
        ts.set_token(TS_TOKEN)
        pro = ts.pro_api()

        # 需要的字段
        fields = TradeCal._meta.fields.keys()
        fields = ','.join([x for x in fields if x not in ('id', 'create_time', 'update_time')])

        # 交易日历
        df = pro.trade_cal(exchange='', start_date='20000101', end_date='20201231', fields=fields)

        model_list = DfToModels.df2models(df, TradeCal)
        TradeCal.delete().execute()
        TradeCal.bulk_create(model_list, 500)


if __name__ == '__main__':
    TsTradeCal.run()
