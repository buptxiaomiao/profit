# coding: utf-8

import tushare as ts

from settings import TOKEN
from utils.db_tools import conn


class TaskFundBasic(object):

    @classmethod
    def run(cls):
        """
        公募基金列表
        https://tushare.pro/document/2?doc_id=19
        :return:
        """
        # 设置ts token
        ts.set_token(TOKEN)
        pro = ts.pro_api()

        field_default = (
            ('ts_code', ''),
            ('name', ''),
            ('management', ''),
            ('custodian', ''),
            ('fund_type', ''),
            ('found_date', ''),
            ('due_date', ''),
            ('list_date', ''),
            ('issue_date', ''),
            ('delist_date', ''),
            ('issue_amount', 0),
            ('m_fee', 0),
            ('c_fee', 0),
            ('duration_year', 0),
            ('p_value', 0),
            ('min_amount', 0),
            ('exp_return', 0),
            ('benchmark', ''),
            ('status', ''),
            ('invest_type', ''),
            ('type', ''),
            ('trustee', ''),
            ('purc_startdate', ''),
            ('redm_startdate', ''),
            ('market', ''),
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
            df = pro.fund_basic(
                fields=fields, offset=offset, limit=limit
            )
            df = df.fillna(dict(field_default))
            for i, row in df.iterrows():
                sql = 'replace into fund_basic ({}) values ({})'.format(','.join(fields), ','.join(['%s'] * len(row)))
                cursor.execute(sql, tuple([x for x in row.values]))

            if df.shape[0] < limit:
                break

            offset += limit

        cursor.execute('alter table fund_basic engine=innodb; ')
        conn.commit()
        cursor.close()
        conn.close()


"""
CREATE TABLE `fund_basic` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(32) NOT NULL DEFAULT '' COMMENT '基金代码',
  `name` char(128) NOT NULL DEFAULT '' COMMENT '简称',
  `management` char(128) NOT NULL DEFAULT '' COMMENT '管理人',
  `custodian` char(128) NOT NULL DEFAULT '' COMMENT '托管人',
  `fund_type` char(32) NOT NULL DEFAULT '' COMMENT '投资类型',
  `found_date` char(32) NOT NULL DEFAULT '' COMMENT '成立日期',
  `due_date` char(32) NOT NULL DEFAULT '' COMMENT '到期日期',
  `list_date` char(32) NOT NULL DEFAULT '' COMMENT '上市时间',
  `issue_date` char(32) NOT NULL DEFAULT '' COMMENT '发行日期',
  `delist_date` char(32) NOT NULL DEFAULT '' COMMENT '退市日期',
  `issue_amount` FLOAT NOT NULL DEFAULT 0 COMMENT '发行份额(亿)',
  `m_fee` FLOAT NOT NULL DEFAULT 0 COMMENT '管理费',
  `c_fee` FLOAT NOT NULL DEFAULT 0 COMMENT '托管费',
  `duration_year` FLOAT NOT NULL DEFAULT 0 COMMENT '存续期',
  `p_value` FLOAT NOT NULL DEFAULT 0 COMMENT '面值',
  `min_amount` FLOAT NOT NULL DEFAULT 0 COMMENT '起点金额(万元)',
  `exp_return` FLOAT NOT NULL DEFAULT 0 COMMENT '预期收益率',
  `benchmark` char(1024) NOT NULL DEFAULT '' COMMENT '	业绩比较基准',
  `status` char(8) NOT NULL DEFAULT '' COMMENT '存续状态D摘牌 I发行 L已上市',
  `invest_type` char(64) NOT NULL DEFAULT '' COMMENT '投资风格',
  `type` char(64) NOT NULL DEFAULT '' COMMENT '基金类型',
  `trustee` char(128) NOT NULL DEFAULT '' COMMENT '受托人',
  `purc_startdate` char(32) NOT NULL DEFAULT '' COMMENT '日常申购起始日',
  `redm_startdate` char(32) NOT NULL DEFAULT '' COMMENT '日常赎回起始日',
  `market` char(8) NOT NULL DEFAULT '' COMMENT '	E场内O场外',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ts_code` (`ts_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公募基金基本信息表'
"""