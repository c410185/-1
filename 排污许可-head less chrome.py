# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep

chromedriver = 'C:\\Users\何方辉\AppData\Local\Google\Chrome\Application\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument('headless')
prefs = {'profile.default_content_settings.popups': 0,
         'download.default_directory': 'C:\DTLDownLoads\\'}
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.get('http://sahitest.com/demo/saveAs.htm')
driver.find_element_by_xpath('/html/body/a[3]').click()
print(driver.title)
sleep(3)
driver.quit()