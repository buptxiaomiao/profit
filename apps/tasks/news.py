# coding: utf-8

import tushare as ts

from settings import TOKEN
from utils.time_tool import TimeTool
from utils.db_tools import conn


class TaskNews(object):

    SRC_LIST = [
        'wallstreetcn',     # 华尔街见闻
        'sina',             # 新浪财经
        '10jqka',           # 同花顺
        'eastmoney',        # 东方财富
        'yuncaijing',       # 云财经
    ]

    @classmethod
    def run(cls, st=None, et=None):
        """
        新闻快讯
        https://tushare.pro/document/2?doc_id=143
        :return:
        """
        et = TimeTool.str_to_datetime(et) or TimeTool.now() + TimeTool.timedelta(minutes=1)
        st = TimeTool.str_to_datetime(st) or et - TimeTool.timedelta(minutes=30)

        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        fields = [
            'datetime',
            'title',
            'content',
            'channels',
        ]

        cursor = conn.cursor()
        cursor.execute(
            'set SESSION autocommit = 0;'
        )

        for src in cls.SRC_LIST:
            df = pro.news(src=src, start_date=st, end_date=et, fields=fields)
            for i, row in df.iterrows():

                d = row.to_dict()
                news_time = d.get('datetime', '0001-01-01 00:00:00') or '0001-01-01 00:00:00'
                title = d.get('title', '') or ''
                content = d.get('content', '') or ''
                content_hash = hash(content)
                channels = d.get('channels', '') or ''

                sql = 'select 1 from news where news_time = %s and content_hash = %s and src= %s;' \
                      % (news_time, content_hash, src)
                cursor.execute(sql)
                res = cursor.fetchall()
                if res:
                    continue

                sql = "replace into " \
                      "news (new_time, title, content, content_hash, channels) " \
                      "values (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (news_time, title, content, content_hash, channels))

        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskNews.run()
