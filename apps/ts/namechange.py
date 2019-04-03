# coding: utf-8

import tushare as ts

from settings.settings import TS_TOKEN
from utils.df_to_models import DfToModels
from models.name_change import NameChange


class TsNameChange(object):

    @classmethod
    def run(cls):
        """
        历史名称变更记录
        https://tushare.pro/document/2?doc_id=100
        :return:
        """
        # 设置ts token
        ts.set_token(TS_TOKEN)
        pro = ts.pro_api()

        # 需要的字段
        fields = NameChange._meta.fields.keys()
        fields = ','.join([x for x in fields if x not in ('id', 'create_time', 'update_time')])

        # 沪
        df = pro.namechange(fields=fields)
        model_list = DfToModels.df2models(df, NameChange)

        NameChange.delete().execute()
        NameChange.bulk_create(model_list, 500)


if __name__ == '__main__':
    TsNameChange.run()
