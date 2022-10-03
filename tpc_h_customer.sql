insert into tpc-h.customer (C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL, C_MKTSEGMENT, C_COMMENT) values (1, 'Magic W', '地址是多少', 1, 18382001006, 12342, '中国', '中国');
insert into tpc-h.customer (C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL, C_MKTSEGMENT, C_COMMENT) values (2, '朴德霜', '地址是多少', 1, 19908020202, 12342, '中国', 'good');

insert into tpc-h.lineitem (L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, L_QUANTITY, L_EXTENDEDPRICE, L_DISCOUNT, L_TAX, L_RETURNFLAG, L_LINESTATUS, L_SHIPDATE, L_COMMITDATE, L_RECEIPTDATE, L_SHIPINSTRUCT, L_SHIPMODE, L_COMMENT) values (1, 2, 1, 2, 70, 119, 0.85, 20, '否', '未', '2018-12-21 00:00:00', '2018-12-29 00:00:00', '2018-12-30 00:00:00', '吨', '船', 3);
insert into tpc-h.lineitem (L_ORDERKEY, L_PARTKEY, L_SUPPKEY, L_LINENUMBER, L_QUANTITY, L_EXTENDEDPRICE, L_DISCOUNT, L_TAX, L_RETURNFLAG, L_LINESTATUS, L_SHIPDATE, L_COMMITDATE, L_RECEIPTDATE, L_SHIPINSTRUCT, L_SHIPMODE, L_COMMENT) values (1, 1, 1, 3, 8, 74.8, 0.85, 20, '否', '未', '1996-01-01 00:00:00', '2018-12-27 00:00:00', '2018-12-30 00:00:00', '吨', '船', 1);

insert into tpc-h.nation (N_NATIONKEY, N_NAME, N_REGIONKEY, N_COMMENT) values (1, '中国', 1, 'good');
insert into tpc-h.nation (N_NATIONKEY, N_NAME, N_REGIONKEY, N_COMMENT) values (2, '英国', 3, 'good');
insert into tpc-h.nation (N_NATIONKEY, N_NAME, N_REGIONKEY, N_COMMENT) values (3, '美国', 4, 'hhhh');
insert into tpc-h.nation (N_NATIONKEY, N_NAME, N_REGIONKEY, N_COMMENT) values (4, '埃及', 2, 3);
insert into tpc-h.nation (N_NATIONKEY, N_NAME, N_REGIONKEY, N_COMMENT) values (5, '澳大利亚', 5, 'hhhh');

insert into tpc-h.orders (O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE, O_ORDERDATE, O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY, O_COMMENT) values (1, 1, 1, 193.8, '2018-12-20 00:00:00', 1, 'j', 1, 'hhhh');
insert into tpc-h.orders (O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE, O_ORDERDATE, O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY, O_COMMENT) values (2, 2, 3, 0, '2018-12-05 00:00:00', 2, 't', 2, 'hhhh');

insert into tpc-h.part (P_PARTKEY, P_NAME, P_MFGR, P_BRAND, P_TYPE, P_SIZE, P_CONTAINER, P_RETAILPRICE, P_COMMENT) values (1, 'a', 1, 'TE', '汽车零件', 3, '周转包装', 11, 'good');
insert into tpc-h.part (P_PARTKEY, P_NAME, P_MFGR, P_BRAND, P_TYPE, P_SIZE, P_CONTAINER, P_RETAILPRICE, P_COMMENT) values (2, 'b', 4, 'TE', '普通零件', 2, '一次性包装', 2, 'good');
insert into tpc-h.part (P_PARTKEY, P_NAME, P_MFGR, P_BRAND, P_TYPE, P_SIZE, P_CONTAINER, P_RETAILPRICE, P_COMMENT) values (3, 'c', 1, 'TE', '电脑零件', 5, '周转包装', 15, 'hhhh');

insert into tpc-h.partsupp (PS_PARTKEY, PS_SUPPKEY, PS_AVAILQTY, PS_SUPPLYCOST, PS_COMMENT) values (1, 1, 1250, 13, 'hhhh');
insert into tpc-h.partsupp (PS_PARTKEY, PS_SUPPKEY, PS_AVAILQTY, PS_SUPPLYCOST, PS_COMMENT) values (2, 2, 1600, 5, 3);

insert into tpc-h.region (R_REGIONKEY, R_NAME, R_COMMENT, PS_SUPPLYCOST, PS_COMMENT) values (1, '亚洲', '哈哈哈', 12, '哈哈哈哈');
insert into tpc-h.region (R_REGIONKEY, R_NAME, R_COMMENT, PS_SUPPLYCOST, PS_COMMENT) values (2, '非洲', '哈哈哈哈', 13, '哈哈哈哈');
insert into tpc-h.region (R_REGIONKEY, R_NAME, R_COMMENT, PS_SUPPLYCOST, PS_COMMENT) values (3, '欧洲', '哈哈哈哈', 15, '哈哈哈哈');
insert into tpc-h.region (R_REGIONKEY, R_NAME, R_COMMENT, PS_SUPPLYCOST, PS_COMMENT) values (4, '美洲', '哈哈哈哈', 33, '哈哈哈哈');
insert into tpc-h.region (R_REGIONKEY, R_NAME, R_COMMENT, PS_SUPPLYCOST, PS_COMMENT) values (5, '大洋洲', '哈哈哈哈', 25, '哈哈哈哈');

insert into tpc-h.supplier (S_SUPPKEY, S_NAME, S_ADDRESS, S_NATIONKEY, S_PHONE, S_ACCTBAL, S_COMMENT) values (1, '潘柳燕', '不知道地址', 1, 18382001006, 23213, '好供应商');
insert into tpc-h.supplier (S_SUPPKEY, S_NAME, S_ADDRESS, S_NATIONKEY, S_PHONE, S_ACCTBAL, S_COMMENT) values (2, '朴德霜', '不知道地址', 1, 19908020202, 112332, 3);
