CREATE TABLE `prod_price` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '记录id',
  `seqno` varchar(16) NOT NULL DEFAULT '' COMMENT '序号',
  `the_day` char(16) NOT NULL DEFAULT '' COMMENT '日期',
  `prod_name` varchar(64) NOT NULL DEFAULT '' COMMENT '产品名称',
  `price` float NOT NULL DEFAULT '0' COMMENT '价格',
  `unit` varchar(64) NOT NULL DEFAULT '' COMMENT '单位',
  `region` varchar(64) NOT NULL DEFAULT '' COMMENT '地区',
  `prod_spec` varchar(128) NOT NULL DEFAULT '' COMMENT '描述',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_seq_day` (`seqno`,`the_day`),
  KEY `prod_day` (`prod_name`,`the_day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品价格'

