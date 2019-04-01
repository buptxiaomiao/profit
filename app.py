# coding: utf-8

import fire


class Script(object):

    @classmethod
    def role_level_exp(cls):
        from scripts.crawl.role_level_exp import RoleLevelExpCrawl
        RoleLevelExpCrawl().main()

    @classmethod
    def role_practice(cls):
        from scripts.crawl.role_practice import RolePracticeCrawl
        RolePracticeCrawl().main()


class App(object):
    
    @classmethod
    def script(cls):
        return Script


if __name__ == '__main__':
    fire.Fire(App())
