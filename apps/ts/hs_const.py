# coding: utf-8

import tushare as ts

from settings.settings import TS_TOKEN
from utils.df_to_models import DfToModels
from models.hs_const import HSConst


class TsHSConst(object):

    @classmethod
    def run(cls):
        """
        沪深股通成份股
        https://tushare.pro/document/2?doc_id=104
        :return:
        """
        # 设置ts token
        ts.set_token(TS_TOKEN)
        pro = ts.pro_api()

        # 需要的字段
        fields = HSConst._meta.fields.keys()
        fields = ','.join([x for x in fields if x not in ('id', 'create_time', 'update_time')])

        # 沪
        df1 = pro.hs_const(hs_type='SH', fields=fields)
        model_list1 = DfToModels.df2models(df1, HSConst)

        # 深
        df2 = pro.hs_const(hs_type='SZ')
        model_list2 = DfToModels.df2models(df2, HSConst)

        HSConst.delete().execute()
        HSConst.bulk_create(model_list1, 500)
        HSConst.bulk_create(model_list2, 500)


if __name__ == '__main__':
    TsHSConst.run()
