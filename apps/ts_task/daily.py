# coding: utf-8

import time
import tushare as ts

from settings import TOKEN
from utils.db_tools import conn
from utils.time_tool import TimeTool

# 设置ts token
ts.set_token(TOKEN)


class TaskDaily(object):

    @classmethod
    def run(cls, st=None, et=None, flag_refresh_all=0):
        """
        日线 通用行情接口
        https://tushare.pro/document/2?doc_id=109
        :return:
        """
        print st, et, flag_refresh_all
        st = TimeTool.str_to_datetime(st) or TimeTool.now(-1)
        et = TimeTool.str_to_datetime(et) or TimeTool.now(1)

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 0;')

        cursor.execute('select ts_code, list_date from stock where is_valid = 1 order by ts_code asc;')
        db_res = cursor.fetchall()

        for stock in db_res:
            ts_code = stock[0]
            list_date = stock[1]
            if flag_refresh_all == 0:
                date_pair = cls.cal_date_pair(st=st, et=et)
            else:
                date_pair = cls.cal_date_pair(st=list_date, et=et)

            for _st, _et in date_pair:
                time.sleep(1.0 / 500)
                cls.save_daily_to_db(ts_code, _st, _et, cursor)
            conn.commit()

        cursor.close()
        conn.close()

    @classmethod
    def save_daily_to_db(cls, ts_code, st, et, cursor):

        # 为了取120天均值
        api_st = str(TimeTool.str_to_datetime(st) - TimeTool.timedelta(days=120))[:10]
        print 'ts_code:{} daily begin, api_st:{}, et:{}'.format(ts_code, api_st, et)

        df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=api_st, end_date=et,
                        ma=[5, 10, 20, 30, 60, 120, 12, 26, 3])

        st_check_format = TimeTool.datetime_to_str(st, '%Y%m%d')
        if df is None or df.empty:
            print 'df is null. ts_code:{}, st:{}, et:{}'.format(ts_code, api_st, et)
            return

        df = df.fillna(0).where(df['trade_date'] >= st_check_format).dropna(axis=0)
        if df is None or df.empty:
            return

        fields = ['ts_code', 'trade_date', 'close', 'open', 'high', 'low', 'pre_close',
                  'change', 'pct_chg', 'vol', 'amount',
                  'ma5', 'ma10', 'ma20', 'ma30', 'ma60', 'ma120',
                  'ma12', 'ma26', 'ma_v_3']
        for i, row in df.iterrows():
            values = [getattr(row, x, '') for x in fields]
            sql = 'replace into daily ({}) values ({})'.format(
                ','.join(['`{}`'.format(f) for f in fields]),
                ','.join(['%s'] * len(fields))
            )
            cursor.execute(sql, tuple(values))

    @classmethod
    def cal_date_pair(cls, st, et, delta=5000):
        st = TimeTool.str_to_datetime(st)
        et = TimeTool.str_to_datetime(et)

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
