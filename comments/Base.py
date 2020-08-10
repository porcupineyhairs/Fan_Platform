# -*- coding: utf-8 -*-
# @Time    : 2019/8/25
# @Author  : cyq
# @File    : Base.py
# @Desc    : 基类方法
import os
import time

from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from comments.log import get_log

import platform

if platform.system() == "Windows":
    DriverPath = os.path.join(os.path.dirname(__file__), "chromedriver7.exe")
else:
    DriverPath = os.path.join(os.path.dirname(__file__), "chromedriver84")


class PageBase:
    f = Faker(locale='zh_CN')

    def __init__(self, headless=None, window_size="1920,1080"):
        self.log = get_log(__name__)

        try:
            opt = webdriver.ChromeOptions()
            # 设置浏览器不提供可视化页面
            # if headless:
            #     opt.add_argument('--headless')
            # 指定浏览器分辨率
            if window_size:
                opt.add_argument('--window-size=' + window_size)
            self.driver = webdriver.Chrome(executable_path=DriverPath, options=opt)
            self.driver.implicitly_wait(10)
        except BaseException as e:
            self.log.exception(e)
            self.log.error('浏览器报错!')
            return

    def get_url(self, url: str):
        """
        打開url
        """
        try:
            self.driver.get(url)
        except Exception as e:
            self.log.error(str(e))
            return None


    def scrollIntoView(self, la: tuple):
        """
        滑动界面
        """
        try:
            ele = self.find_element(la)
            if ele:
                self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        except Exception as e:
            self.log.error(str(e))
            return None

    def go_back(self):
        self.driver.back()

    def set_Browser_size(self):
        """
        默认全屏
        """
        try:
            self.driver.maximize_window()
        except Exception as e:
            self.log.error(str(e))
            return None

    def quit_Browser(self):
        """
        退出Browser
        """
        try:
            self.driver.quit()
        except Exception as e:
            self.log.error(str(e))
            return None

    def ActionChainsClick(self, locator: tuple):
        """
        模擬鼠标点击
        """
        try:
            element = self.find_element(locator)
            if element:
                ActionChains(self.driver).move_to_element(element).click().perform()
        except Exception as e:
            self.log.error(str(e))
            return None

    def ActionChainsSend_Keys(self, locator: tuple, key: str):
        """
        模拟鼠标录入
        """

        try:
            element = self.find_element(locator)
            if element:
                ActionChains(self.driver).move_to_element(element).click().send_keys(key).perform()
        except Exception as e:
            self.log.error(str(e))
            return None

    def ActionChainsOffsetClick(self, x, y, element=None):
        """
        坐标点击
        """
        try:
            if element:
                ActionChains(self.driver).move_to_element_with_offset(element, 0, 0).perform()
                time.sleep(1)
            ActionChains(self.driver).move_by_offset(x, y).perform()
        except Exception as e:
            self.log.error(str(e))
            self.log.error("坐标错误")
            return None

    def Js_clear(self, locator):
        """
        js clear input
        """
        try:
            self.click(locator)
            js = f'document.querySelector("#{locator[1]}").value="";'
            self.driver.execute_script(js)
        except Exception as e:
            self.log.error(e)

    def getMsg(self):
        return self.get_text(('xpath', '//div[@class="ant-message"]/span'))

    def get_url(self, url):
        """
        go url
        """
        try:
            self.driver.get(url)
        except Exception as e:
            self.log.error(str(e))
            return None

    def find_elements(self, locator: tuple, timeout=10):
        """
        定位一組元素,
        """
        try:
            element = WebDriverWait(self.driver, timeout, 10).until(EC.presence_of_all_elements_located(locator))
            return element
        except Exception as e:
            self.log.error("未找到: {}".format(locator[1]))
            self.log.error(str(e))
            return []

    def find_element(self, locator: tuple, timeout=10):
        """
        定位元素,
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            time.sleep(0.5)
            return element
        except Exception as e:
            self.log.error("未找到: {}".format(locator[1]))
            return None

    def click(self, locator: tuple):
        """
        点击
        """
        element = self.find_element(locator)
        try:
            if element:
                element.click()
        except Exception as e:
            self.log.error(str(e))
            self.log.error(f"{locator} 点击失败")
            return

    def refresh(self):
        """
        刷新
        """
        self.driver.refresh()

    def clear(self, locator: tuple):
        """
        清空
        """
        try:
            ele = self.find_element(locator)
            ele.send_keys(Keys.CONTROL, "a")
            ele.send_keys(Keys.DELETE)
        except TimeoutException:
            self.log.error("clear失敗 {}".format(str(locator)))
            return False

    def get_text(self, locator: tuple, timeout=3):
        """
        获取文本
        """
        try:
            element = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(locator))
            return element.text
        except TimeoutException:
            self.log.error('元素 {element} 没有找到'.format(element=locator))
            return None

    def get_attribute(self, locator: tuple, name: str):
        """
        获取属性
        """
        element = self.find_element(locator)
        return element.get_attribute(name)


    def send_keys(self, locator: tuple, text: str):
        """
        传参
        """
        element = self.find_element(locator)
        if element:
            try:
                element.clear()
                element.send_keys(text)
            except WebDriverException as e:
                self.log.error(str(e))
                self.log.error('元素  {element}不可编辑'.format(element=locator))
                return

    def switch_to_window(self, new_window=None):
        """
        切换新窗口
        :param new_window: 新窗口句柄
        :return: 当前窗口句柄
        """
        if new_window is None:
            current_handle = self.driver.window_handles
            try:
                self.driver.switch_to.window(current_handle[-1])
                return current_handle
            except TimeoutException as e:
                self.log.error("切换窗口失败或无新窗口被打开, 无需切换窗口")
                raise e
        else:
            self.driver.switch_to.window(new_window)

    def Get_Png(self):
        """
        获取当前窗口的屏幕截图作为二进制数据
        """
        return self.driver.get_screenshot_as_png()


if __name__ == '__main__':
    print(DriverPath)
