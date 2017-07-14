# -*- coding:utf-8 -*-

import time
import traceback
import MySQLdb as mydb
from xlogging import log

from lib_crawl import do_crawl
from crawl_exception import RobotCheckError, OperationError

DB_HOST = 'localhost'
# DB_HOST = '107.167.179.14'
DB_USER = 'amzuser'
DB_PASSWD = '7B1YxSAhyILb'
DB_DB = 'amazon_crawl'

SQL_ALL_ASIN = """
                SELECT asin FROM  `crawl_asin` WHERE  `id` >=1  ORDER BY  `id` ASC 
                """

SQL_INSERT_STAT = """
                    INSERT into crawl_asin_statistic VALUES (NULL, '%s', '%s', '%s');
                    """

Max_Num_Msg = 'exceeded the maximum number of items'

log.setConfig(module_name='crawl_amazon_manual', ro_rotateby=2, ro_when='midnight', \
              ro_backupcount=4, logfile='crawl_amazon_manual.log')

if __name__ == '__main__':
    # connect to db
    try:
        conn = mydb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_DB)
        curs = conn.cursor()
        num = curs.execute(SQL_ALL_ASIN)

        info = curs.fetchmany(num)

        asin_list = []
        for item in info:
            asin = item[0]
            asin_list.append(asin)
    except Exception, e:
        log.critical('Get ALL Asin Failed: %s' % traceback.format_exc())
        print 'Get Asin failed'
        conn.close()

    # do crawl
    for asin in asin_list:
        print 'Start Crawl ', asin
        log.info('Start Crawl %s' %asin)
        try:
            q, msg = do_crawl(asin, is_proxy=0)
            if msg.find(Max_Num_Msg) > 0:
                q = 1000
        except RobotCheckError, e:
            print 'Crawl %s faild: %s' % (asin, traceback.format_exc())
            log.critical("crawl %s failed: %s" % (asin, traceback.format_exc()))
            q = -1
        except OperationError, e:
            print 'Crawl %s faild: %s' % (asin, traceback.format_exc())
            log.critical("crawl %s failed: %s" % (asin, traceback.format_exc()))
            q = -1


        '''
        sql = SQL_INSERT_STAT % (asin, int(q), str(datetime.date.today()))
        curs.execute(sql)
        conn.commit()
        '''
        print 'Finish Crawl ', asin
        log.info('Finish Crawl %s' % asin)
        time.sleep(0.5)
    conn.close()
