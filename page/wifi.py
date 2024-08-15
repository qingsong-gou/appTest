# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/14 11:11
@Auth ： qsgou
@File ：wifi.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import time

from page.setting import SettingPage
from utils.event import Event


class WifiPage():
    def __init__(self):
        self.device = Event()._gain_device()
        self.setting_page = SettingPage(self.device)  # 设置页面
        self.setting_page.click_wifi()  # 点击进入wifi页面
        time.sleep(8)
        self.driver = self.setting_page.driver  # driver

    def get_connect_wifi_stats(self):
        flag = False
        try:
            if self.driver.wait_until_element_found_by_resourceId_text(
                    param="com.iflytek.ainote.settings:id/wifi_status",
                    text="已连接"):
                flag = True
        except Exception as e:
            pass
        finally:
            return flag

    def click_add_manually(self):
        element = self.driver.wait_until_element_found_by_resourceId(
            param="com.iflytek.ainote.settings:id/add_network")
        element.click()
        time.sleep(5)
        return element

    def click_security(self):
        element1 = self.driver.wait_until_element_found_by_resourceId_text(
            param="com.iflytek.ainote.settings:id/tv_summary_security",
            text="无")
        element1.click()
        time.sleep(2)
        element2 = self.driver.wait_until_element_found_by_resourceId_text(
            param="com.iflytek.ainote.settings:id/tv_text",
            text="WPA/WPA2 PSK")
        element2.click()
        time.sleep(2)
        return element2

    def input_wifi_name(self, value):
        self.driver.clear_input_by_resourceId(
            location="com.iflytek.ainote.settings:id/wifi_name_edit",
            value=value)
        time.sleep(1)

    def input_wifi_password(self, value):
        self.driver.clear_input_by_resourceId(
            location="com.iflytek.ainote.settings:id/password_edit",
            value=value)
        time.sleep(1)

    def click_connect(self):
        element = self.driver.wait_until_element_found_by_resourceId(
            param="com.iflytek.ainote.settings:id/btn_connect")
        element.click()
        time.sleep(5)
        return element

    def check_title(self):
        flag = False
        try:
            if self.driver.wait_until_element_found_by_resourceId_text(
                    param="com.iflytek.ainote.settings:id/tv_title",
                    text="WIFI设置"):
                flag = True
        except Exception as e:
            pass
        finally:
            return flag


if __name__ == '__main__':
    wifi_page = WifiPage()
    # wifi_page.click_add_manually()
    # wifi_page.click_security()
    # wifi_page.input_wifi_name()
    # wifi_page.input_wifi_password()
    # wifi_page.click_connect()
    # if wifi_page.get_connect_wifi_stats():
    #     print(111)
