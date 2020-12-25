# coding: utf-8

import tushare as ts
import time

from settings import TOKEN
from utils.db_tools import conn


class TaskFundPortfolio(object):

    @classmethod
    def run(cls):
        """
        公募基金列表
        https://tushare.pro/document/2?doc_id=121
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        field_default = (
            ('ts_code', ''),
            ('ann_date', ''),
            ('end_date', ''),
            ('symbol', ''),
            ('mkv', 0),
            ('amount', 0),
            ('stk_mkv_ratio', 0),
            ('stk_float_ratio', 0)
        )

        fields = [i[0] for i in field_default]

        cursor = conn.cursor()
        cursor.execute(
            'set SESSION autocommit = 0;'
        )

        cursor.execute('select ts_code, list_date from fund_basic order by ts_code asc;')
        db_res = cursor.fetchall()

        for fund in db_res:
            ts_code = fund[0]

            df = pro.fund_portfolio(
                fields=fields, ts_code=ts_code
            )
            df = df.fillna(dict(field_default))
            for i, row in df.iterrows():
                sql = 'replace into fund_portfolio ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
                cursor.execute(sql, tuple([x for x in row.values]))

            conn.commit()
            time.sleep(0.05)

        cursor.execute('alter table fund_portfolio engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    TaskFundPortfolio.run()

"""
CREATE TABLE `fund_portfolio` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(32) NOT NULL DEFAULT '' COMMENT 'TS基金代码',
  `ann_date` char(32) NOT NULL DEFAULT '' COMMENT '公告日期',
  `end_date` char(32) NOT NULL DEFAULT '' COMMENT '截止日期',
  `symbol` char(64) NOT NULL DEFAULT '' COMMENT '股票代码',
  
  `mkv` FLOAT NOT NULL DEFAULT 0 COMMENT '发行份额(亿)',
  `amount` FLOAT NOT NULL DEFAULT 0 COMMENT '管理费',
  `stk_mkv_ratio` FLOAT NOT NULL DEFAULT 0 COMMENT '托管费',
  `stk_float_ratio` FLOAT NOT NULL DEFAULT 0 COMMENT '存续期',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ts_code` (`ts_code`, `end_date`, `symbol`),
  KEY `idx_symbol` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公募基金持仓数据'
"""