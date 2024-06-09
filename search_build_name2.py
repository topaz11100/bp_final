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
DELAY_TIME = 2

class kakao_map():
    def __init__(self, mode = "no"):
        self.mode = mode
        self.url = "https://map.kakao.com/"
        
    def __openweb(self):
        if self.mode == "no":
            options = wb.ChromeOptions()
            options.add_argument('headless')
            self.browser = wb.Chrome(options=options)
        else:
            self.browser = wb.Chrome()
        self.browser.get(self.url)
        time.sleep(DELAY_TIME)
    
    def __enter__(self):
        self.__openweb()
        return self
    
    def __inputclear(self, search_box):
        search_box.clear()
        search_box.clear()
        search_box.clear()
        search_box.clear()
        WebDriverWait(self.browser, DELAY_TIME).until(
        EC.text_to_be_present_in_element_value((By.ID, "search.keyword.query"), "") )
        
    def __stayLoad(self):
        while(True):
            try:
                addr = self.browser.find_element(By.CLASS_NAME, "link_addr")
            except:
                continue
            else:
                return
   
    def __search(self, address):
        search_box = self.browser.find_element(By.ID, "search.keyword.query")
        
        while search_box.get_attribute("value"):
            self.__inputclear(search_box)
        
        search_box.send_keys(address)
        search_box.send_keys(Keys.RETURN)
        
        self.__stayLoad()

    def find_name(self, addr, road_addr):
        if "산" in addr:
            return "산"
        if "지하" in road_addr:
            return "지하철"
        self.__search(addr)
        try:
            postage = self.browser.find_element(By.CLASS_NAME, "zip")
        except NoSuchElementException:
            return "nozip"
        else:
            postnum = postage.text
            self.__search(road_addr)
            try:
                buildname = self.browser.find_element(By.CLASS_NAME, "building")
            except NoSuchElementException:
                return postnum
            else:
                return buildname.text
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.quit()
    
def search_to_csv(data, file_path, mode="no"):
    with kakao_map(mode) as browser:
        for i in range(len(data.index)):
            data.iloc[i, 4] = browser.find_name(data.iloc[i, 2], data.iloc[i, 3])
            print(file_path[16:16+3], i)
    data.to_csv(file_path, index=False, encoding=encoding)

