# coding: utf-8

import tushare as ts

from settings.settings import TS_TOKEN
from utils.df_to_models import DfToModels
from models.stock import Stock


class TsStockBasic(object):

    @classmethod
    def run(cls):
        """
        股票列表
        https://tushare.pro/document/2?doc_id=25
        :return:
        """
        # 设置ts token
        ts.set_token(TS_TOKEN)
        pro = ts.pro_api()

        # 需要的字段
        fields = Stock._meta.fields.keys()
        fields = ','.join([x for x in fields if x not in ('id', 'create_time', 'update_time')])

        # 上市
        df1 = pro.stock_basic(
            list_status='L', fields=fields
        )
        model_list1 = DfToModels.df2models(df1, Stock)

        # 退市
        df2 = pro.stock_basic(
            list_status='D', fields=fields
        )
        model_list2 = DfToModels.df2models(df2, Stock)

        # 暂停上市
        df3 = pro.stock_basic(
            list_status='P', fields=fields
        )
        model_list3 = DfToModels.df2models(df3, Stock)

        Stock.delete().execute()
        Stock.bulk_create(model_list1, 500)
        Stock.bulk_create(model_list2, 500)
        Stock.bulk_create(model_list3, 500)


if __name__ == '__main__':
    TsStockBasic.run()
