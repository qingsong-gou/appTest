# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/14 10:18
@Auth ： qsgou
@File ：setting.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import time

from utils.base import Base
from utils.event import Event

device = Event()._gain_device()


class SettingPage():
    def __init__(self, device):
        self.driver = Base(device)
        self.driver.press_home()  # 返回主页
        self.driver.click_x_by_resourceId('com.toycloud.launcher:id/iv_settings')  # 直接进入设置页面
        time.sleep(3)

    def click_airplane_mode(self):
        self.driver.click_x_by_resourceId(location='com.iflytek.ainote.settings:id/switch_view')
        time.sleep(2)

    def get_disable(self):
        '''
        触发飞行模式后出现的元素
        :return:
        '''
        if self.driver.exist_by_resourceId(param='com.iflytek.ainote.settings:id/summary'):
            return True

    def click_wifi(self):
        element = self.driver.wait_until_element_found_by_resourceId_text(param="com.iflytek.ainote.settings:id/title",
                                                                          text="WLAN")
        element.click()


if __name__ == '__main__':
    set_page = SettingPage(device=device)
    set_page.click_airplane_mode()
    set_page.click_wifi()
