# coding: utf-8

import numpy as np

import tushare as ts
from settings import TOKEN
from utils.db_tools import conn
from utils.time_tool import TimeTool


class TaskMoneyFlowHsgt(object):

    @classmethod
    def run(cls, year=None):
        """
        沪深港通资金流向
        https://tushare.pro/document/2?doc_id=47
        :return:
        """
        if year:
            st = TimeTool.datetime(year=year, month=1, day=1)
        else:
            st = TimeTool.datetime(year=TimeTool.now().year, month=1, day=1)
        et = st + TimeTool.timedelta(days=366)

        st = TimeTool.datetime_to_str(st, '%Y%m%d')
        et = TimeTool.datetime_to_str(et, '%Y%m%d')

        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        fields = [
            'trade_date',
            'ggt_ss',
            'ggt_sz',
            'hgt',
            'sgt',
            'north_money',
            'south_money'
        ]

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 1;')

        # 上市公司基本信息
        df = pro.moneyflow_hsgt(start_date=st, end_date=et)
        for i, row in df.iterrows():
            sql = 'replace into moneyflow_hsgt ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            try:
                # print sql, row.values
                cursor.execute(sql, tuple([x if x is not np.nan else 0 for x in row.values]))
            except Exception as e:
                print row.values
                print np.nan_to_num(row.values)

        cursor.execute('alter table moneyflow_hsgt engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskMoneyFlowHsgt.run()

"""
CREATE TABLE `moneyflow_hsgt` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `trade_date` char(32) NOT NULL DEFAULT '' COMMENT '交易日期',
  `ggt_ss` float NOT NULL DEFAULT '0' COMMENT '港股通（上海）',
  `ggt_sz` float NOT NULL DEFAULT '0' COMMENT '港股通（深圳）',
  `hgt` float NOT NULL DEFAULT '0' COMMENT '沪股通（百万元）',
  `sgt` float NOT NULL DEFAULT '0' COMMENT '深股通（百万元）',
  `north_money` float NOT NULL DEFAULT '0' COMMENT '北向资金（百万元）',
  `south_money` float NOT NULL DEFAULT '0' COMMENT '南向资金（百万元）',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `trade_date` (`trade_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='moneyflow_hsgt沪深港通资金流向'
"""