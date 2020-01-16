# coding: utf-8

import time
import tushare as ts
from settings import TOKEN
from utils.db_tools import conn


class TaskNameChange(object):

    @classmethod
    def run(cls, ts_code=''):
        """
        历史名称变更记录
        https://tushare.pro/document/2?doc_id=100
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        # 需要的字段
        fields = [
            'ts_code',
            'name',
            'start_date',
            'end_date',
            'ann_date',
            'change_reason'
        ]

        cursor = conn.cursor()
        cursor.execute('select ts_code, list_date from stock where ts_code >= %s order by ts_code asc;', (ts_code, ))
        res = cursor.fetchall()
        cursor.execute('set SESSION autocommit = 0;')
        for x in res:

            ts_code = x[0]
            # 名称变更记录
            time.sleep(0.3)
            try:
                df = pro.namechange(ts_code=ts_code, fields=fields)
            except Exception as e:
                print e.message
                time.sleep(60)
                df = pro.namechange(ts_code=ts_code, fields=fields)

            for i, row in df.iterrows():
                sql = 'replace into namechange ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
                print sql, row.values
                cursor.execute(sql, tuple([x or '' for x in row.values]))
            conn.commit()

        cursor.execute('alter table namechange engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskNameChange.run()
