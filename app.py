# coding: utf-8

import sys
import fire
reload(sys)
sys.setdefaultencoding('utf-8')


class App(object):

    @classmethod
    def daily(cls):
        from apps.ts.daily import TsDaily
        TsDaily.run()

    @classmethod
    def ts_task(cls):
        from apps.ts_task import TsTask
        return TsTask

    @classmethod
    def monitor_task(cls):
        from apps.monitor_task import MonitorTask
        return MonitorTask

    @classmethod
    def price_task(cls):
        from apps.price_task import PriceTask
        return PriceTask()



if __name__ == '__main__':
    fire.Fire(App())
