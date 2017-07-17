# -*- coding:utf-8 -*-

import time
import traceback
from xlogging import log
import pdb

from lib_captcha import parse_captcha
from crawl_exception import RobotCheckError, OperationError

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.common.by import By

def do_crawl(asin, is_proxy=0, no_pic=1):
    chrome_options = webdriver.ChromeOptions()
    if is_proxy == 1:
        # set proxy
        chrome_options.add_argument(('--proxy-server=socks5://127.0.0.1:6060'))

    '''
    chrome_options.add_argument(("--disable-plugins"))
    chrome_options.add_argument(("--disable-images"))
    chrome_options.add_argument(("--start-maximized"))
    chrome_options.add_argument(("--disable-javascript"))
    '''

    if no_pic == 1:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # go to the Amazon home page
    driver.implicitly_wait(10)
    try:
        driver.get("https://www.amazon.com")
    except Exception:
        print 'Load the Landing Page Timeout'
        raise OperationError("Load the Landing Page Timeout")

    #time.sleep(6000)
    loading = 0
    ix = 0
    while ix < 10:
        if driver.title.find('Robot Check') != -1: #Robot Check
            captcha_element = driver.find_element(By.XPATH,
                                                  '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
            url = captcha_element.get_attribute('src')
            print url
            #log.info('url: %s' % url)
            captcha_text = parse_captcha(url)
            print captcha_text
            #log.info('captcha: %s' % captcha_text)
            #pdb.set_trace()
            rc_input = driver.find_element_by_id('captchacharacters')
            time.sleep(0.5)
            rc_input.send_keys(captcha_text)
            time.sleep(0.5)
            rc_input.submit()
            ix += 1
        elif driver.title.find('Amazon') != -1: # Good to Landing Page
            print 'Landing Page Loaded'
            loading = 1
            break
        else:   # Error
            print 'Landing Page Load Failed'
            #driver.save_screenshot("codingpy.png")
            driver.quit()
            raise RobotCheckError("Load Landing Page Unknow Error")

    if loading ==0 and driver.title.find('Amazon') != -1: # Good to Landing Page
        print 'Landing Page Loaded'
        loading = 1
    '''
    try:
        element = WebDriverWait(driver, 10).until(EC.title_contains('Robot Check'))
        #pdb.set_trace()
        captcha_element = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
        url = captcha_element.get_attribute('src')
        print url
        log.info('url: %s' % url)
        captcha_text = parse_captcha(url)
        print captcha_text
        log.info('captcha: %s' %captcha_text)
        pdb.set_trace()
        rc_input = driver.find_element_by_id('captchacharacters')
        rc_input.send_keys(captcha_text)
        rc_input.submit()
    except Exception ,e:
        traceback.print_exc()

    try:
        element = WebDriverWait(driver, 10).until(EC.title_contains('Amazon'))
        print 'Landing Page Loaded'
    except Exception, e:
        print 'Landing Page Load Failed'
        traceback.format_exc()
        driver.save_screenshot("codingpy.png")
        driver.quit()
        return -1, ''
        '''

    if loading:
        inputElement = driver.find_element_by_name("field-keywords")
        inputElement.send_keys(asin)
        inputElement.submit()
    else:  # Error
        print 'Pass Robot Check Failed'
        driver.quit()
        raise RobotCheckError("Captcha Failed")

    try:
        element = WebDriverWait(driver, 10).until(EC.title_contains('Amazon'))
        print 'ASIN %s Found' % asin
    except:
        print 'ASIN %s Search Failed' % asin
        driver.quit()
        raise OperationError("ASIN %s Search Failed" % asin)

    print 'click item'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result_0"]/div/div/div/div[2]/div[1]/div[1]/a')))
        element.click()
    except Exception, e:
        print 'Search Result not clickable'
        driver.quit()
        raise OperationError("Search Result not clickable")

    # 点击加入购物车
    print 'add item into cart'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'add-to-cart-button')))
        element.click()
    except Exception, e:
        print 'add item to cart failed'
        driver.save_screenshot("codingpy.png")
        driver.quit()
        raise OperationError("add item to cart failed")

    # 进入购物车
    print 'go into cart'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'hlb-view-cart-announce')))
        element.click()
    except Exception, e:
        print 'go into cart failed'
        driver.quit()
        raise OperationError("go into cart failed")

    # 找到购物车里的商品
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="a-autoid-2"]')))
        element.click()
    except Exception, e:
        print 'Click Quantity Failed'
        driver.quit()
        raise OperationError("Click Quantity Failed")

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'dropdown1_9')))
        element.click()
    except Exception, e:
        print 'Click 9+ Failed'
        driver.quit()
        raise OperationError("Click 9+ Failed")

    time.sleep(2)
    input_element = driver.find_element(By.XPATH,
                                        '//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div/div[3]/div/div/input')
    input_element.send_keys(999)

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'a-autoid-3-announce')))
        element.click()
    except Exception, e:
        print 'Click Update_Botton Failed'
        driver.quit()
        raise OperationError("Click Update_Botton Failed")

    print 'sleep 2s'
    time.sleep(5)
    input_element = driver.find_element(By.XPATH,
                                        '//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div/div[3]/div/div/input')
    print "ASIN: ", asin
    q = input_element.get_attribute('value')
    print q
    try:
        msg = driver.find_element(By.XPATH, '//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div[1]/div/div/div/span').text
    except Exception, e:
        msg = '>=999'
    print 'warning message:'
    print msg
    driver.quit()
    return (q, msg)


def do_crawl_pjs(asin, is_proxy=0, no_pic=1):
    driver = webdriver.PhantomJS(executable_path='/Users/kieslee/workspace/selenium/phantomjs/bin/phantomjs')

    # go to the Amazon home page
    try:
        driver.get("https://www.amazon.com")
    except Exception:
        print 'Load the Landing Page Timeout'
        pass

    try:
        element = WebDriverWait(driver, 10).until(EC.title_contains('Amazon'))
        print 'Landing Page Loaded'
    except Exception, e:
        print 'Landing Page Load Failed'
        traceback.format_exc()
        driver.save_screenshot("codingpy.png")
        driver.quit()
        return -1, ''

    inputElement = driver.find_element_by_name("field-keywords")
    inputElement.send_keys(asin)
    inputElement.submit()

    try:
        element = WebDriverWait(driver, 10).until(EC.title_contains('Amazon'))
        print 'ASIN %s Found' % asin
    except:
        print 'ASIN %s Search Failed' % asin
        print driver.title
        driver.quit()
        return -1, ''

    print 'click item'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result_0"]/div/div/div/div[2]/div[1]/div[1]/a')))
        element.click()
    except Exception, e:
        print 'Search Result not clickable'
        driver.quit()
        return -1, ''

    # 点击加入购物车
    print 'add item into cart'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'add-to-cart-button')))
        element.click()
    except Exception, e:
        print 'add item to cart failed'
        driver.quit()
        return -1, ''

    # 进入购物车
    print 'go into cart'
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'hlb-view-cart-announce')))
        element.click()
    except Exception, e:
        print 'go into cart failed'
        driver.quit()
        return -1, ''

    # 找到购物车里的商品
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="a-autoid-2"]')))
        element.click()
    except Exception, e:
        print 'Click Quantity'
        driver.quit()
        return -1, ''

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'dropdown1_9')))
        element.click()
    except Exception, e:
        print 'Click 9+'
        driver.quit()
        return -1, ''

    time.sleep(2)
    input_element = driver.find_element(By.XPATH,
                                        '//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div/div[3]/div/div/input')
    input_element.send_keys(999)

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'a-autoid-3-announce')))
        element.click()
    except Exception, e:
        print 'Click Update_Botton Failed'
        driver.quit()
        return -1, ''

    print 'sleep 2s'
    time.sleep(5)
    input_element = driver.find_element(By.XPATH,
                                        '//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div/div[3]/div/div/input')
    print "ASIN: ", asin
    q = input_element.get_attribute('value')
    print q
    try:
        msg = driver.find_element(By.XPATH, '//*[@id="activeCartViewForm"]/div[2]/div/div[4]/div[1]/div/div/div/span').text
    except Exception, e:
        msg = '>=999'
    print 'warning message:'
    print msg
    driver.quit()
    return (q, msg)


def get_info_by_asin(asin):
    pass
