# coding: utf-8

import tushare as ts

from settings import TOKEN
from utils.db_tools import conn


class TaskTradeCal(object):

    @classmethod
    def run(cls, st=None, et=None):
        """
        交易日历
        https://tushare.pro/document/2?doc_id=26
        :param st: 20190101
        :param et: 20201231
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        fields = [
            'exchange',
            'cal_date',
            'is_open',
            'pretrade_date',
        ]

        kwargs = {}
        if st:
            kwargs.update(start_date=st)
        if et:
            kwargs.update(start_date=et)

        # 交易日历
        df = pro.trade_cal(fields=fields, **kwargs)

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 0;')

        for i, row in df.iterrows():
            sql = 'replace into trade_cal ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            print sql, row.values
            cursor.execute(sql, tuple([x or '' for x in row.values]))
        cursor.execute("""
            UPDATE trade_cal a
            JOIN ( SELECT * FROM trade_cal WHERE is_open = 1 ) t ON ( t.pretrade_date = a.cal_date ) 
            SET a.nexttrade_date = t.cal_date 
            WHERE
                a.is_open = 1;
        """)
        cursor.execute('alter table trade_cal engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskTradeCal.run()
