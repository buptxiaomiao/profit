# coding: utf-8

from peewee import MySQLDatabase
from peewee import OperationalError
from peewee import __exception_wrapper__
from peewee import Model
from peewee import DoesNotExist
from peewee import chunked

from utils.log_tools import logger
from settings.settings import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


class MyRetryDb(MySQLDatabase):

    def execute_sql(self, sql, params=None, commit=True):
        try:
            cursor = super(MyRetryDb, self).execute_sql(
                sql, params, commit)
        except OperationalError:
            if not self.is_closed():
                self._state.transactions = []
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        return cursor


def get_mysql_client(host='localhost', port=3306, user='', password='', db='profit'):
    return MyRetryDb(host=host, port=port, user=user, password=password, database=db)


db = get_mysql_client(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)


class BaseModel(Model):

    class Meta:
        database = db

    @classmethod
    def get_one(cls, *query, **kwargs):
        try:
            return cls.get(*query, **kwargs)
        except DoesNotExist:
            return None

    @classmethod
    def batch_insert(cls, dict_list, nums=1000):
        """批量创建"""
        if not dict_list:
            return
        for batch in chunked(dict_list, nums):
            cls.insert_many(batch).execute()
        print 'insert {} rows:{}'.format(cls.__name__.lower(), len(dict_list))
        return
