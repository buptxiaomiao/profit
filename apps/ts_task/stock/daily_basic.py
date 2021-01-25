# coding: utf-8

import tushare as ts

from settings import TOKEN
from utils.db_tools import conn
from utils.time_tool import TimeTool


class TaskDailyBasic(object):

    @classmethod
    def run_by_period(cls, st, et):
        st = TimeTool.str_to_datetime(st)
        et = TimeTool.str_to_datetime(et)
        if not (st and et) or st < et:
            print 'st:{}, et:{} is invalid.'
            return

        st = TimeTool.datetime_to_str(st, '%Y%m%d')
        et = TimeTool.datetime_to_str(et, '%Y%m%d')

        t = et
        while t >= st:
            trade_date = TimeTool.datetime_to_str(t, '%Y%m%d')
            cls.run(trade_date=trade_date)
            t -= TimeTool.timedelta(days=1)

    @classmethod
    def run(cls, trade_date):
        """
        沪深股票 每日指标
        https://tushare.pro/document/2?doc_id=32
        :return:
        """
        trade_date = TimeTool.str_to_datetime(trade_date) or TimeTool.date_to_datetime(TimeTool.now())
        trade_date = TimeTool.datetime_to_str(trade_date, '%Y%m%d')

        print 'begin task stock-daily-basic. trade_date:{}'.format(trade_date)
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        field_default = (
            ('ts_code', ''),        # TS股票代码
            ('trade_date', ''),     # 交易日期
            ('close', 0),           # 当日收盘价
            ('turnover_rate', 0),   # 换手率（%）
            ('turnover_rate_f', 0), # 换手率（自由流通股）
            ('volume_ratio', 0),    # 量比
            ('pe', 0),              # 市盈率（总市值/净利润， 亏损的PE为空）
            ('pe_ttm', 0),          # 市盈率（TTM，亏损的PE为空）
            ('pb', 0),              # 市净率（总市值/净资产）
            ('ps', 0),              # 市销率
            ('ps_ttm', 0),          # 市销率（TTM）
            ('dv_ratio', 0),        # 股息率 （%）
            ('dv_ttm', 0),          # 股息率（TTM）（%）
            ('total_share', 0),     # 总股本 （万股）
            ('float_share', 0),     # 流通股本 （万股）
            ('free_share', 0),      # 自由流通股本 （万）
            ('total_mv', 0),        # 总市值 （万元）
            ('circ_mv', 0),         # 流通市值（万元）
        )

        fields = [i[0] for i in field_default]

        cursor = conn.cursor()
        cursor.execute(
            'set SESSION autocommit = 0;'
        )

        offset = 0
        limit = 5000
        while 1:
            # 上市
            df = pro.daily_basic(
                trade_date=trade_date, fields=fields, offset=offset, limit=limit
            )
            df = df.fillna(dict(field_default))
            for i, row in df.iterrows():
                sql = 'replace into daily_basic ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
                cursor.execute(sql, tuple([x for x in row.values]))

            if df.shape[0] < limit:
                break

            offset += limit

        cursor.execute('alter table daily_basic engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()
        print 'finish task stock-daily-basic. trade_date:{}'.format(trade_date)


"""

CREATE TABLE `daily_basic` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(32) NOT NULL DEFAULT '' COMMENT 'TS股票代码',
  `trade_date` char(32) NOT NULL DEFAULT '' COMMENT '交易日期',
  `close` FLOAT NOT NULL DEFAULT 0 COMMENT '当日收盘价',
  `turnover_rate` FLOAT NOT NULL DEFAULT 0 COMMENT '换手率（%）',
  `turnover_rate_f` FLOAT NOT NULL DEFAULT 0 COMMENT '换手率（自由流通股）',
  `volume_ratio` FLOAT NOT NULL DEFAULT 0 COMMENT '量比',
  `pe` FLOAT NOT NULL DEFAULT 0 COMMENT '市盈率（总市值/净利润， 亏损的PE为空）',
  `pe_ttm` FLOAT NOT NULL DEFAULT 0 COMMENT '市盈率（TTM，亏损的PE为空）',
  `pb` FLOAT NOT NULL DEFAULT 0 COMMENT '市净率（总市值/净资产）',
  `ps` FLOAT NOT NULL DEFAULT 0 COMMENT '市销率',
  `ps_ttm` FLOAT NOT NULL DEFAULT 0 COMMENT '市销率（TTM）',
  `dv_ratio` FLOAT NOT NULL DEFAULT 0 COMMENT '股息率 （%）',
  `dv_ttm` FLOAT NOT NULL DEFAULT 0 COMMENT '股息率（TTM）（%）',
  `total_share` FLOAT NOT NULL DEFAULT 0 COMMENT '总股本 （万股）',
  `float_share` FLOAT NOT NULL DEFAULT 0 COMMENT '流通股本 （万股）',
  `free_share` FLOAT NOT NULL DEFAULT 0 COMMENT '自由流通股本 （万）',
  `total_mv` FLOAT NOT NULL DEFAULT 0 COMMENT '总市值 （万元）',
  `circ_mv` FLOAT NOT NULL DEFAULT 0 COMMENT '流通市值（万元）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_trade_date_ts_code` (`trade_date`, `ts_code`),
  KEY `idx_ts_code` (`ts_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='沪深股票每日指标'

"""