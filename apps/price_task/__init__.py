# coding: utf-8

from apps.price_task.prod_price import ProdPrice


class PriceTask(object):

    @classmethod
    def prod_price(cls):
        return ProdPrice()

