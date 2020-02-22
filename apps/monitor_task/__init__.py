# coding: utf-8

from apps.monitor_task.news_mail import NewsMail


class MonitorTask(object):

    @classmethod
    def mail_news(cls):
        return NewsMail.run()

