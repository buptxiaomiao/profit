# coding: utf-8

import time
import json
import requests

from utils.db_tools import conn
from utils.time_tool import TimeTool


class ProdPrice(object):

    API = 'http://price.mofcom.gov.cn/datamofcom/front/price/pricequotation/priceQueryList'

    @classmethod
    def run(cls, st=None, et=None):
        et = TimeTool.str_to_datetime(et) or TimeTool.now()
        st = TimeTool.str_to_datetime(st) or et - TimeTool.timedelta(days=7)

        et = TimeTool.datetime_to_str(et, '%Y%m%d')
        st = TimeTool.datetime_to_str(st, '%Y%m%d')
        cls.main(st, et)

    @classmethod
    def main(cls, st='', et=''):

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 0;')

        for i in xrange(1, 400):
            data = {
                'seqno': i,
                'startTime': st,
                'endTime': et,
                'pageNumber': 1,
                'pageSize': 10000,
            }
            time.sleep(1)
            print cls.API, data
            res = requests.post(cls.API, data)
            content = json.loads(res.content)
            rows = content.get('rows')
            for x in rows:

                region = x.get('region', '')
                yyyy = x.get('yyyy', '')
                mm = x.get('mm', '')
                dd = x.get('dd', '')
                unit = x.get('unit', '')
                price = x.get('price', '0')
                prod_spec = x.get('prod_spec', '')
                prod_name = x.get('prod_name', '')

                the_day = '{}-{}-{}'.format(yyyy, mm, dd)
                info = {
                    'seqno': i,
                    'the_day': the_day,
                    'prod_name': prod_name,
                    'price': price,
                    'unit': unit,
                    'region': region,
                    'prod_spec': prod_spec,
                }
                cls.save_db(info, 'prod_price', cursor)
            conn.commit()
        conn.close()

    @classmethod
    def save_db(cls, info, table, _cursor):
        print info
        columns = []
        values = []
        for k, v in info.iteritems():
            columns.append(k)
            values.append(v)

        sql = "replace into {} ({}) values ({})".format(
            table,
            ','.join(['`{}`'.format(i) for i in columns]),
            ','.join(['%s'] * len(values))
        )
        # print sql
        # print tuple([str(i) for i in values])
        _cursor.execute(sql, tuple(values))
