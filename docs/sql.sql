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
  `nexttrade_date` char(16) NOT NULL DEFAULT '' COMMENT '下个交易日',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ex_cal` (`cal_date`,`exchange`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易日历'


CREATE TABLE `namechange` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(16) NOT NULL DEFAULT '' COMMENT 'TS代码',
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '证券名称',
  `start_date` char(16) NOT NULL DEFAULT '' COMMENT '开始日期',
  `end_date` char(16) NOT NULL DEFAULT '' COMMENT '结束日期',
  `ann_date` char(16) NOT NULL DEFAULT '' COMMENT '公告日期',
  `change_reason` char(128) NOT NULL DEFAULT '' COMMENT '变更原因',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ts_code` (`ts_code`,`start_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='股票曾用名'


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


CREATE TABLE `daily` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `ts_code` char(16) NOT NULL DEFAULT '' COMMENT 'TS代码',
  `trade_date` int(11) NOT NULL DEFAULT '0' COMMENT '交易日期',
  `open` float NOT NULL DEFAULT '0' COMMENT '开盘价',
  `high` float NOT NULL DEFAULT '0' COMMENT '最高价',
  `low` float NOT NULL DEFAULT '0' COMMENT '最低价',
  `close` float NOT NULL DEFAULT '0' COMMENT '收盘价',
  `pre_close` float NOT NULL DEFAULT '0' COMMENT '昨收价',
  `change` float NOT NULL DEFAULT '0' COMMENT '涨跌额',
  `pct_chg` float NOT NULL DEFAULT '0' COMMENT '涨跌幅',
  `vol` float NOT NULL DEFAULT '0' COMMENT '成交量（手）',
  `amount` float NOT NULL DEFAULT '0' COMMENT '成交额 （千元）',
  `ma2` float NOT NULL DEFAULT '0' COMMENT '2日均价',
  `ma5` float NOT NULL DEFAULT '0' COMMENT '5日均价',
  `ma10` float NOT NULL DEFAULT '0' COMMENT '10日均价',
  `ma12` float NOT NULL DEFAULT '0' COMMENT '12日均价',
  `ma26` float NOT NULL DEFAULT '0' COMMENT '26日均价',
  `ma30` float NOT NULL DEFAULT '0' COMMENT '30日均价',
  `ma60` float NOT NULL DEFAULT '0' COMMENT '60日均价',
  `ma120` float NOT NULL DEFAULT '0' COMMENT '120日均价',
  `ma250` float NOT NULL DEFAULT '0' COMMENT '250日均价',
  `ma_v_2` float NOT NULL DEFAULT '0',
  `ma_v_5` float NOT NULL DEFAULT '0',
  `ma_v_10` float NOT NULL DEFAULT '0',
  `ma_v_12` float NOT NULL DEFAULT '0',
  `ma_v_26` float NOT NULL DEFAULT '0',
  `ma_v_30` float NOT NULL DEFAULT '0',
  `ma_v_60` float NOT NULL DEFAULT '0',
  `ma_v_120` float NOT NULL DEFAULT '0',
  `ma_v_250` float NOT NULL DEFAULT '0',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `ts_code_trade_date` (`ts_code`,`trade_date`),
  KEY `trade_date_ts_code` (`trade_date`,`ts_code`)
) ENGINE=InnoDB AUTO_INCREMENT=9642 DEFAULT CHARSET=utf8mb4 COMMENT='A股非创业板日线'


CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `src` char(16) NOT NULL DEFAULT '' COMMENT '来源',
  `news_time` datetime NOT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '新闻时间',
  `title` text COMMENT '标题',
  `content` mediumtext COMMENT '内容',
  `content_hash` bigint(20) NOT NULL DEFAULT '0' COMMENT '内容hash',
  `channels` text COMMENT '分类',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `time_hash_src` (`news_time`,`content_hash`,`src`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='新闻简讯'
