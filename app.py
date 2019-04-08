# coding: utf-8

import fire


class App(object):

    @classmethod
    def daily(cls):
        from apps.ts.daily import TsDaily
        TsDaily.run()


if __name__ == '__main__':
    fire.Fire(App())
