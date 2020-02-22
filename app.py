# coding: utf-8

import fire


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


if __name__ == '__main__':
    fire.Fire(App())
