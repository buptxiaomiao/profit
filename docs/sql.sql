CREATE TABLE `stock` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(32) NOT NULL DEFAULT '' COMMENT 'TS代码',
  `symbol` char(32) NOT NULL DEFAULT '' COMMENT '股票代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '股票名称',
  `area` char(16) NOT NULL DEFAULT '' COMMENT '所在地域',
  `industry` char(32) NOT NULL DEFAULT '' COMMENT '所属行业',
  `market` varchar(32) NOT NULL DEFAULT '' COMMENT '主板/中小板/创业板',
  `exchange` varchar(32) NOT NULL DEFAULT '' COMMENT '交易所代码',
  `list_status` char(8) NOT NULL DEFAULT '' COMMENT 'L上市 D退市 P暂停上市',
  `list_date` char(32) NOT NULL DEFAULT '' COMMENT '上市时间',
  `is_hs` char(8) NOT NULL DEFAULT '' COMMENT '是否沪深港通标的，N否 H沪股通 S深股通',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ts_code` (`ts_code`),
  KEY `symbol` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=21707 DEFAULT CHARSET=utf8mb4 COMMENT='stock基本信息表'


CREATE TABLE `trade_cal` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `exchange` char(8) NOT NULL DEFAULT '' COMMENT '交易所代码, SSE上交所 SZSE深交所',
  `cal_date` char(16) NOT NULL DEFAULT '' COMMENT '日历日期, 如20191231',
  `is_open` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否交易 0休市 1交易',
  `pretrade_date` char(16) NOT NULL DEFAULT '' COMMENT '上一个交易日',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `is_open_cal_date` (`is_open`,`cal_date`)
) ENGINE=InnoDB AUTO_INCREMENT=7306 DEFAULT CHARSET=utf8mb4 COMMENT='交易日历'


CREATE TABLE `hs_const` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(16) NOT NULL DEFAULT '' COMMENT 'TS代码',
  `hs_type` char(8) NOT NULL DEFAULT '' COMMENT '沪深港通类型SH沪SZ深',
  `in_date` char(16) NOT NULL DEFAULT '' COMMENT '纳入日期',
  `out_date` char(16) NOT NULL DEFAULT '' COMMENT '剔除日期',
  `is_new` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否最新 1是 0否',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ts_code` (`ts_code`),
  KEY `hs_type` (`hs_type`),
  KEY `in_date` (`in_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='沪深股通成份股'


CREATE TABLE `namechange` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(16) NOT NULL DEFAULT '' COMMENT 'TS代码',
  `name` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '证券名称',
  `start_date` char(16) NOT NULL DEFAULT '' COMMENT '开始日期',
  `end_date` char(16) NOT NULL DEFAULT '' COMMENT '结束日期',
  `change_reason` CHAR(128) NOT NULL DEFAULT '' COMMENT '变更原因',
  `ann_date` char(16) NOT NULL DEFAULT '' COMMENT '公告日期',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ts_code` (`ts_code`),
  KEY `start_date` (`start_date`)
) ENGINE=InnoDB AUTO_INCREMENT=1318 DEFAULT CHARSET=utf8mb4 COMMENT='股票曾用名'

