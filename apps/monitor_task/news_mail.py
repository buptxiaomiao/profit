# coding: utf-8

from utils.time_tool import TimeTool
from utils.db_tools import conn
from utils.mail_tools import MailTools


class NewsMail(object):

    SRC_MAP = {
        'wallstreetcn': u'华尔街见闻',
        'sina': u'新浪财经',
        '10jqka': u'同花顺',
        'eastmoney': u'东方财富',
        'yuncaijing': u'云财经'
    }

    @classmethod
    def run(cls):

        cursor = conn.cursor()
        cursor.execute('select substr(news_time, 1, 19) as news_time, src, content from news '
                       'where news_time >= date_sub(now(), interval 60 minute) '
                       'order by news_time desc limit 500;')
        res = cursor.fetchall()

        mail_list = []
        for x in res:
            news_time = x[0]
            src = x[1]
            content = x[2]
            src_name = cls.SRC_MAP.get(src, '')

            msg =  u'{}   {}\n' \
                   u'{}\n'.format(news_time, src_name, content)
            # print msg
            mail_list.append(
               msg
            )

        mail_content = '-------------------------\n'.join(mail_list)
        MailTools.send_mail(
            subject=u'新闻简讯-{}'.format(TimeTool.datetime_to_str(TimeTool.now(), '%m-%d %H:%M')),
            content=mail_content
        )
