# coding: utf-8

from apps.tasks.stock import TaskStockBasic


class Task(object):

    @classmethod
    def stock(cls):
        return TaskStockBasic.run()
