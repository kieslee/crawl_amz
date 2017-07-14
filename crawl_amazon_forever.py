# -*- coding:utf-8 -*-

import datetime
import traceback
import time
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
                SELECT asin FROM  `crawl_asin` ORDER BY  `id` ASC 
                """

SQL_INSERT_STAT = """
                    INSERT into crawl_asin_statistic VALUES (NULL, '%s', '%s', '%s');
                    """

Max_Num_Msg = 'exceeded the maximum number of items'

START_HOUR = 15

log.setConfig(module_name='crawl_amazon_forever', ro_rotateby=2, ro_when='midnight', \
              ro_backupcount=4,logfile='crawl_amazon_forever.log')

if __name__ == '__main__':
    today_done = 0
    while True:
        current_time = time.localtime(time.time())
        if current_time.tm_hour != START_HOUR:
            if today_done == 1 and current_time.tm_hour > START_HOUR:
                today_done = 0
            time.sleep(30)
        elif today_done == 1:
            time.sleep(30)
        else:
            #print 'Start do Crawl at ', datetime.datetime.now()
            log.info('Start do Crawl at %s' % str(datetime.datetime.now()))
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
                conn.close()
                continue

            # do crawl
            for asin in asin_list:
                try:
                    log.info('Start Crawl %s' % asin)
                    q, msg = do_crawl(asin)
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

                try:
                    sql = SQL_INSERT_STAT % (asin, int(q), str(datetime.date.today()))
                    curs.execute(sql)
                    conn.commit()
                    log.info('Crawl %s Succ' % asin)
                except Exception, e:
                    log.critical("Crawl %s failed: %s" %(asin, traceback.format_exc()))


            conn.close()
            today_done = 1
            print 'Finish Crawl at ', datetime.datetime.now()
            log.info('Finish Crawl at %s', str(datetime.datetime.now()))
