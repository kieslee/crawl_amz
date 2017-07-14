# -*- coding:utf-8 -*-

import datetime
import MySQLdb as mydb

from lib_crawl import do_crawl

#DB_HOST = 'localhost'
DB_HOST = '107.167.179.14'
DB_USER = 'amzuser'
DB_PASSWD = '7B1YxSAhyILb'
DB_DB = 'amazon_crawl'

asin = 'B00ED8O3P8'

SQL_INSERT_STAT = """
                    INSERT into crawl_asin_statistic VALUES (NULL, '%s', '%s', '%s');
                    """

Max_Num_Msg = 'exceeded the maximum number of items'

if __name__ == '__main__':
    # connect to db
    conn = mydb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_DB)

    # do crawl
    print 'Start Crawl ', asin
    q, msg = do_crawl(asin, is_proxy=1)
    if msg.find(Max_Num_Msg) > 0:
        q = 1000
    if q == -1:
        print 'Crawl %s faild' % asin

    sql = SQL_INSERT_STAT % (asin, int(q), str(datetime.date.today()))
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()

    conn.close()
