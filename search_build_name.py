#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 멀티프로세싱 위한 검색 모듈
import numpy as np
import pandas as pd

import time

from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

encoding = "cp949"
DELAY_TIME = 5
map_url = "https://map.kakao.com/"

def openweb(mode):
    if mode == "no":
        options = wb.ChromeOptions()
        options.add_argument('headless')
        driver = wb.Chrome(options=options)
    else:
        driver = wb.Chrome()
    driver.get(map_url)
    time.sleep(DELAY_TIME)
    return driver

class browser_kakaomap():
    def __init__(self, mode = "no"):
        self.mode = mode
    def __enter__(self):
        self.browser = openweb(self.mode)
        return self.browser
    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.quit()
        
def inputclear(browser):
    search_box = browser.find_element(By.ID, "search.keyword.query")
    while search_box.get_attribute("value"):
        search_box.send_keys(Keys.CONTROL, 'a')
        search_box.send_keys(Keys.BACKSPACE)

def stayforLoad(browser):
    while(True):
        try:
            addr = browser.find_element(By.CLASS_NAME, "link_addr")
        except NoSuchElementException:
            inputclear(browser)
            continue
        else:
            return
        
def search(browser, address):
    search_box = browser.find_element(By.ID, "search.keyword.query")
    inputclear(browser)
    search_box.send_keys(address)
    search_box.send_keys(Keys.RETURN)
    wait = WebDriverWait(browser, DELAY_TIME)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'link_addr')))
    
def find_name(browser, addr, road_addr):
    if "산" in addr:
        return "산"
    if "지하" in road_addr:
        return "지하철"
    search(browser, addr)
    try:
        postage = browser.find_element(By.CLASS_NAME, "zip")
    except NoSuchElementException:
        return "nozip"
    else:
        postnum = postage.text
        search(browser, road_addr)
        try:
            buildname = browser.find_element(By.CLASS_NAME, "building")
        except NoSuchElementException:
            return postnum
        else:
            return buildname.text
        
def search_to_csv(data, file_path):
    with browser_kakaomap("no") as browser:
        for i in range(len(data.index)):
            print(file_path[16:16+4], i)
            data.iloc[i, 4] = find_name(browser, data.iloc[i, 2], data.iloc[i, 3])
    data.to_csv(file_path, index=False, encoding=encoding)

