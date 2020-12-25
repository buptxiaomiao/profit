# coding: utf-8

import tushare as ts
import time

from settings import TOKEN
from utils.db_tools import conn
from utils.time_tool import TimeTool


class TaskFundPortfolio(object):

    @classmethod
    def run(cls, incr=1):
        """
        公募基金列表
        https://tushare.pro/document/2?doc_id=121
        :return:
        """
        # 这里的start_date通过ann_date进行的筛选.
        start_date = TimeTool.datetime_to_str(TimeTool.now(-15), '%Y%m%d') if incr else ''

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

        q_kwargs = {}
        if start_date:
            q_kwargs['start_date'] = start_date

        for fund in db_res:
            ts_code = fund[0]

            df = pro.fund_portfolio(
                fields=fields, ts_code=ts_code, **q_kwargs
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