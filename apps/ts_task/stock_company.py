# coding: utf-8

import tushare as ts
import time

from settings import TOKEN
from utils.db_tools import conn


class TaskStockCompany(object):

    @classmethod
    def run(cls):
        """
        股票列表
        https://tushare.pro/document/2?doc_id=112
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        fields = [
            'ts_code',
            'exchange',
            'chairman',
            'manager',
            'secretary',
            'reg_capital',
            'setup_date',
            'province',
            'city',
            'introduction',
            'website',
            'email',
            'office',
            'business_scope',
            'employees',
            'main_business'
        ]

        cursor = conn.cursor()
        cursor.execute('set SESSION autocommit = 1;')

        # 上市公司基本信息
        df = pro.stock_company(fields=fields)
        for i, row in df.iterrows():
            sql = 'replace into stock_company ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
            try:
                # print sql, row.values
                cursor.execute(sql, tuple([x or '' for x in row.values]))
            except Exception as e:
                print row.values

        cursor.execute('alter table stock_company engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskStockCompany.run()

"""
CREATE TABLE `stock_company` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(32) NOT NULL DEFAULT '' COMMENT 'TS代码',
  `exchange` varchar(32) NOT NULL DEFAULT '' COMMENT '交易所代码',
  `chairman` varchar(64) NOT NULL DEFAULT '' COMMENT '法人代表',
  `manager` varchar(64) NOT NULL DEFAULT '' COMMENT '总经理',
  `secretary` varchar(64) NOT NULL DEFAULT '' COMMENT '董秘',
  `reg_capital` float NOT NULL DEFAULT '0' COMMENT '注册资本',
  `setup_date` varchar(32) NOT NULL DEFAULT '' COMMENT '注册日期',
  `province` varchar(32) NOT NULL DEFAULT '' COMMENT '所在省份',
  `city` varchar(64) NOT NULL DEFAULT '' COMMENT '所在城市',
  `introduction` mediumtext NOT NULL COMMENT '公司介绍',
  `website` text NOT NULL COMMENT '公司主页',
  `email` varchar(64) NOT NULL DEFAULT '' COMMENT '电子邮件',
  `office` text NOT NULL COMMENT '办公室',
  `employees` int(11) NOT NULL DEFAULT '0' COMMENT '员工人数',
  `main_business` mediumtext NOT NULL COMMENT '主要业务及产品',
  `business_scope` mediumtext NOT NULL COMMENT '经营范围',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_valid` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ts_code` (`ts_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='stock_company上市公司基本信息'
"""
