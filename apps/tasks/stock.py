# coding: utf-8

import tushare as ts

from settings import TOKEN
from utils.db_tools import conn


class TaskStockBasic(object):

    @classmethod
    def run(cls):
        """
        股票列表
        https://tushare.pro/document/2?doc_id=25
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        fields = [
            'ts_code',
            'symbol',
            'name',
            'area',
            'industry',
            'market',
            'exchange',
            'list_status',
            'list_date',
            'is_hs'
        ]

        cursor = conn.cursor()

        cursor.execute(
            'set SESSION autocommit = 0;'
        )
        # 上市
        df = pro.stock_basic(
            list_status='L', fields=fields
        )
        for i, row in df.iterrows():
            sql = 'replace into stock ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            print sql, row.values
            cursor.execute(sql, tuple([x or '' for x in row.values]))
        cursor.execute("update stock set is_valid	= 0 where market in ('创业板', '科创板') or name like '%%ST%%'")

        cursor.execute('alter table trade_cal engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskStockBasic.run()
