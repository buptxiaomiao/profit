# coding: utf-8

import time
import tushare as ts

from settings import TOKEN
from utils.db_tools import conn
from utils.time_tool import TimeTool


class TaskDaily(object):

    @classmethod
    def run(cls, st=None, et=None, flag_refresh_all=0):
        """
        日线 通用行情接口
        https://tushare.pro/document/2?doc_id=109
        :return:
        """
        st = TimeTool.str_to_datetime(st) or TimeTool.now(-1)
        et = TimeTool.str_to_datetime(et) or TimeTool.now(1)

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 0;')

        db_res = cursor.execute('select ts_code, list_date from stock where is_valid = 1')
        for stock in db_res:
            ts_code = stock[0]
            list_date = stock[1]
            if flag_refresh_all == 0:
                date_pair = cls.cal_date_pair(st=list_date)
            else:
                date_pair = cls.cal_date_pair(st=st, et=et)
            for st, et in date_pair:
                time.sleep(1.0 / 500)
                cls.save_daily_to_db(ts_code, st, et, cursor)
            conn.commit()

        cursor.close()
        conn.close()

    @classmethod
    def save_daily_to_db(cls, ts_code, st, et, cursor):
        # 设置ts token
        ts.set_token(TOKEN)
        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=st, end_date=et,
                        ma=[5, 10, 20, 30, 60, 120, 12, 26, 3])
        fields = ['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'pre_close',
                  'change', 'pct_chg', 'vol', 'amount',
                  'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120',
                  'ma12', 'ma26', 'ma_v_3']
        df.fillna(0)
        for i, row in df.iterrows():
            values = [getattr(row, x, '') for x in fields]
            sql = 'replace into daily ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            print sql, row.values
            cursor.execute(sql, tuple(values))

    @classmethod
    def cal_date_pair(cls, st, et=None, delta=5000):
        st = TimeTool.str_to_datetime(st)
        et = TimeTool.str_to_datetime(et) or TimeTool.now(1)

        l = []
        tmp_st = st
        while tmp_st < et:
            tmp_et = tmp_st + TimeTool.timedelta(days=delta)
            l.append(
                (str(tmp_st)[:10], str(tmp_et)[:10])
            )
            tmp_st = tmp_et
        return l


if __name__ == '__main__':
    TaskDaily.run()
