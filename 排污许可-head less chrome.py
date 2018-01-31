# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

chromedriver = 'C:\\Users\ipe\PycharmProjects\\untitled\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
prefs = {'profile.default_content_settings.popups': 0,
         'download.default_directory': 'C:\DTLDownLoads\\'}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.get('http://222.143.24.250:98/')
m = driver.find_element_by_xpath('//*[@id="UpdatePanel2"]/div[3]/table/tbody')
table_tr_list = m.find_elements_by_tag_name('tr')
for tr in table_tr_list:
    print(tr.text)
sleep(3)
for i in range(33):
    driver.find_element_by_xpath('//*[@id="asp_enpnomon"]/table/tbody/tr/td[1]/a[3]').click()
    # 显式等待不能识别元素的改变，sleep5秒也不行，到了20秒可以正常获得点击后更新的数据，说明是资源加载的问题。
    sleep(20)
    s = driver.find_element_by_class_name('bjb_bg2')
    table_tr_list1 = s.find_elements_by_tag_name('tr')
    for tr in table_tr_list1:
        print(tr.text)
    sleep(2)
driver.quit()
