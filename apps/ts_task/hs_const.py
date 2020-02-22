# coding: utf-8

import tushare as ts

from settings import TOKEN
from utils.db_tools import conn


class TaskHSConst(object):

    @classmethod
    def run(cls):
        """
        沪深股通成份股
        https://tushare.pro/document/2?doc_id=104
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        # 需要的字段
        fields = [
            'ts_code',
            'hs_type',
            'in_date',
            'out_date',
            'is_new'
        ]

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 0;')

        # 沪
        df = pro.hs_const(hs_type='SH', fields=fields)

        for i, row in df.iterrows():
            sql = 'replace into hs_const ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            print sql, row.values
            cursor.execute(sql, tuple([x or '' for x in row.values]))

        # 深
        df = pro.hs_const(hs_type='SZ', fields=fields)
        for i, row in df.iterrows():
            sql = 'replace into hs_const ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            print sql, row.values
            cursor.execute(sql, tuple([x or '' for x in row.values]))

        cursor.execute('alter table hs_const engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskHSConst.run()
