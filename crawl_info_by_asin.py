# -*- coding:utf-8 -*-

import datetime
import time
import json
import MySQLdb as mydb

from lib_crawl import get_info_by_asin
from lib_cache import list_len, l_pop

#DB_HOST = 'localhost'
DB_HOST = '107.167.179.14'
DB_USER = 'amzuser'
DB_PASSWD = '7B1YxSAhyILb'
DB_DB = 'amazon_crawl'

ASIN_LIST = 'asin_list'


SQL_INSERT_STAT = """
                    INSERT into crawl_asin_statistic VALUES (NULL, '%s', '%s', '%s');
                    """

Max_Num_Msg = 'exceeded the maximum number of items'

if __name__ == '__main__':
    # connect to db
    conn = mydb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_DB)

    asin_info = l_pop(ASIN_LIST)
    asin_info_dict = json.loads(asin_info)
    asin = asin_info_dict['asin']
    try:
        type = asin_info_dict['type']
    except Exception, e:
        type = 'general'
    (url, title) = get_info_by_asin(asin)

    sql = SQL_INSERT_STAT % (asin, int(q), str(datetime.date.today()))
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()

    conn.close()
