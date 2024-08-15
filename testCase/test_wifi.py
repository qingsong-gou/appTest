# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/14 15:08
@Auth ： qsgou
@File ：test_wifi.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import logging

import pytest

from page.wifi import WifiPage
from utils.operationData import OperationExcelData

oper = OperationExcelData(filename="wifi_data.xlsx", sheet_name=0)
wifi_data_success = oper.get_data_to_list()
oper2 = OperationExcelData(filename="wifi_data.xlsx", sheet_name=1)
wifi_data_fail = oper2.get_data_to_list()


class TestWifi():
    def setup_class(self):
        self.wifi_page = WifiPage()  # 类前

    # @pytest.mark.parametrize(['name', 'password', 'description'], wifi_data_success)
    # def test_add_manually_success(self, name, password, description):
    #     logging.info('在wifi页点击手动添加按钮')
    #     self.wifi_page.click_add_manually()
    #     logging.info('选择 WPA/WPA2 PSK ')
    #     self.wifi_page.click_security()
    #     # print(name,password,description)
    #     self.wifi_page.input_wifi_name(value=name)
    #     self.wifi_page.input_wifi_password(value=password)
    #     logging.info('点击立即连接按钮')
    #     self.wifi_page.click_connect()
    #     logging.info('断言连接状态')
    #     assert self.wifi_page.get_connect_wifi_stats()

    @pytest.mark.parametrize(['name', 'password', 'description'], wifi_data_fail)
    def test_add_manually_fail(self, name, password, description):
        logging.info('在wifi页点击手动添加按钮')
        self.wifi_page.click_add_manually()
        logging.info('选择 WPA/WPA2 PSK ')
        self.wifi_page.click_security()
        self.wifi_page.input_wifi_name(value=name)
        self.wifi_page.input_wifi_password(value=password)
        logging.info('点击立即连接按钮')
        self.wifi_page.click_connect()
        logging.info('断言连接状态')
        assert self.wifi_page.get_connect_wifi_stats()


# @pytest.mark.smoke
# def test_wifi_page_element():
#     '''
#     测试wifi页面标志性元素
#     :return:
#     '''
#     logging.info('测试日志')
#     wifi_page = WifiPage()
#     assert wifi_page.check_title()


if __name__ == '__main__':
    # pytest.main(['-vs', './testCase/test_wifi.py', '-m=smoke'])
    pytest.main(['-vs', './testCase/test_wifi.py'])
    # print(wifi_data_fail)
    # print(wifi_data_success)
