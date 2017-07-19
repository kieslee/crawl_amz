# -*- coding:utf-8 -*-

import datetime
import MySQLdb as mydb

from lib_crawl import do_crawl
from conf import use_proxy, DB_HOST, DB_USER, DB_PASSWD, DB_DB


asin = 'B01MQF39OO'

SQL_INSERT_STAT = """
                    INSERT into crawl_asin_statistic VALUES (NULL, '%s', '%s', '%s');
                    """

Max_Num_Msg = 'exceeded the maximum number of items'

if __name__ == '__main__':
    # connect to db
    conn = mydb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_DB)

    # do crawl
    print 'Start Crawl ', asin
    q, msg = do_crawl(asin, is_proxy=use_proxy)
    if msg.find(Max_Num_Msg) > 0:
        q = 1000
    if q == -1:
        print 'Crawl %s faild' % asin


    sql = SQL_INSERT_STAT % (asin, int(q), str(datetime.date.today()))
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()

    conn.close()
