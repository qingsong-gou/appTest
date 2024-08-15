"""
    基类，大概率不变的东西放在基类
    例如，框架本身的东西，或者自己封装的公用方法
"""
import os
# from datetime import time
from time import sleep, time
import uiautomator2 as u2


class Base:
    def __init__(self, device):
        self.driver = u2.connect(device)
        if not self.driver.info['screenOn']:
            self.driver.screen_on()  # 初始化时自动调起亮屏
        # self.appPackage = 'com.iflytek.aistudy.eink.interactiveeffect'

    # def start_app(self):
    #     '''
    #         开启应用
    #     :return:
    #     '''
    #     self.driver.app_start(self.appPackage)
    #     sleep(8)  # 启动app需时间

    # def clear(self):
    #     """
    #         清除app缓存
    #     """
    #     self.driver.app_clear(self.appPackage)
    #
    # def stop(self):
    #     """
    #         关闭App
    #     """
    #     self.driver.app_stop(self.appPackage)
    def back(self, num=1):
        '''
            点击返回
        :param num: 次数
        :return:
        '''

        for i in range(num):
            self.driver.press('back')
            sleep(0.5)

    def clear_input_x_by_resourceId(self, location, value, x):
        """
            清空已填写的选项，重新传值
            :param location: 元素定位字符串
            :param value： 重新传的值
            :param x ：索引
            :return:
        """
        self.driver(resourceId=location)[x].click()  # 定位到元素
        self.driver(focused=True).clear_text()
        self.driver.send_keys(value)

    def clear_input_by_resourceId(self, location, value):
        """
            清空已填写的选项，重新传值
            :param location: 元素定位字符串
            :param value： 重新传的值
        """
        element = self.driver(resourceId=location)
        while not element:
            element = self.driver(resourceId=location)

        element.click()  # 定位到元素
        sleep(1)
        element.clear_text()
        sleep(1)
        element.send_keys(value)
        sleep(1)
        return element

    def close_popup(self, text, locationType, location):
        """
            关闭弹窗
            :param text：字符串，弹窗包含的text文本
            :param locationType：定位方式 xpath or resourceId
            :param location：定位元素字符串，例："//*[@text='登录']"
        """
        element = self.driver(text=text)
        while True:
            if element:
                element.click()
                continue
            else:
                print("权限校验弹窗不存在")
                break
        if locationType == "xpath":
            self.driver.xpath(location).click()
        elif locationType == "resourceId":
            self.driver(resourceId=location).click()

    def swipe_until_element_found(self, param, wait_after_found=0.0, **kwargs):
        """
        检查元素是否存在，若不存在则进行上滑，滑动后再次检查，直到滑动到页面底部
        若找到元素则返回，否则滑动到页面底部后，仍未找到元素，则抛出异常，提示找不到元素
        :param param: xpath字符串 或 元素对象
        :param wait_after_found: 找到元素后，原地等待时间
        :param kwargs:
        :return:
        """
        element = self.driver.xpath(param) if isinstance(param, str) else param
        param = param if isinstance(param, str) else param.selector
        while True:
            try:
                assert element.exists
                if wait_after_found:
                    print("Element found，sleep {} seconds".format(wait_after_found))
                sleep(wait_after_found)
                return element
            except AssertionError:
                print("Element 【 {} 】 Not found, Continue to swipe up...".format(param))
                # 获取滑动前页面下半部分的所有元素
                page_content = self.driver.dump_hierarchy()[(len(self.driver.dump_hierarchy()) // 2):]
                # self.up(**kwargs)
                self.driver.swipe_ext("up")
                sleep(0.5)
                # 获取滑动后页面下半部分的所有元素，并与上一次滑动前的页面元素对比，页面元素没有变化时跳出循环
                if self.driver.dump_hierarchy()[(len(self.driver.dump_hierarchy()) // 2):] == page_content:
                    break
        if not element.exists:
            raise AssertionError("Element 【 {} 】 located failed in this page".format(param))

    def swipe_for_click(self, param, wait_after_click=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则持续向上滑动到底部，直到UI元素在页面内出现，再进行点击
        :param param: xpath字符串 或 元素对象
        :param wait_after_click: 点击后等待时间
        :return:
        """
        element = self.swipe_until_element_found(param, **kwargs)
        element.click()
        if wait_after_click:
            print("Element found and click，then sleep {} seconds".format(wait_after_click))
        sleep(wait_after_click)

    def up(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        上滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.driver.swipe_ext("up", scale, duration=duration, **kwargs)

    def down(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        下滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.driver.swipe_ext("down", scale, duration=duration, **kwargs)

    def left(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        左滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.driver.swipe_ext("left", scale, duration=duration, **kwargs)

    def right(self, scale=0.9, times=1, duration=1.0, **kwargs):
        """
        右滑操作
        :param scale: 滑动单位，默认0.9个单位
        :param times: 滑动次数，默认1次
        :param duration: 滑动时间，默认1.0秒
        :return:
        """
        for i in range(times):
            self.driver.swipe_ext("right", scale, duration=duration, **kwargs)

    def wait_until_element_found_by_xpath(self, param, timeout=30.0, retry_interval=2, wait_after_found=0.0):
        """
        定位元素，如果不存在就间隔若干秒后重试，直到元素定位成功或超时
        :param param: xpath字符串 或 元素对象
        :param timeout: 超时, 默认30秒
        :param retry_interval: 间隔时间, 默认2秒
        :param wait_after_found: 找到元素后，原地等待时间
        :return:
        """
        element = self.driver.xpath(param) if isinstance(param, str) else param
        max_time = time() + timeout
        while True:
            try:
                assert element.exists
                if wait_after_found:
                    print("Element found，then sleep {} seconds".format(wait_after_found))
                sleep(wait_after_found)
                return element
            except AssertionError:
                param = param if isinstance(param, str) else param.selector
                print("Element 【 {} 】 Not found, Retry...".format(param))
                if time() > max_time > 0:
                    raise AssertionError("Element 【 {} 】 located failed after {} timeout".format(param, timeout))
                sleep(retry_interval)

    def wait_until_element_found_by_resourceId(self, param, timeout=30.0, retry_interval=2,
                                               wait_after_found=0.0):
        """
        定位元素，如果不存在就间隔若干秒后重试，直到元素定位成功或超时
        :param param: xpath字符串 或 元素对象
        :param timeout: 超时, 默认30秒
        :param retry_interval: 间隔时间, 默认2秒
        :param wait_after_found: 找到元素后，原地等待时间
        :return:
        """
        element = self.driver(resourceId=param) if isinstance(param, str) else param
        max_time = time() + timeout
        while True:
            try:
                if element.exists:
                    return element
            except AssertionError:
                # param = param if isinstance(param, str) else param.selector
                # print("Element 【 {} 】 Not found, Retry...".format(param))
                if time() > max_time > 0:
                    raise AssertionError("Element 【 {} 】 located failed after {} timeout".format(param, timeout))
                sleep(retry_interval)

    def wait_for_click(self, param, wait_after_click=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则等待UI元素在一定时间内出现，再进行点击
        :param param: xpath字符串 或 元素对象
        :param wait_after_click: 点击后等待时间
        :return:
        """
        element = self.wait_until_element_found_by_resourceId(param, **kwargs)
        element.click()
        if wait_after_click:
            print("Element found and click，then sleep {} seconds".format(wait_after_click))
        sleep(wait_after_click)

    def repeat_click(self, param, times, wait_after_repeat_click=0.0):
        """
        重复多次点击UI元素
        :param param: xpath字符串 或 元素对象
        :param times: 点击次数
        :param wait_after_repeat_click: 重复点击后等待时间，默认为0.0
        :return:
        """
        element = self.wait_until_element_found_by_resourceId(param)
        for i in range(times):
            element.click()
        if wait_after_repeat_click:
            print("Element click，then sleep {} seconds".format(wait_after_repeat_click))
        sleep(wait_after_repeat_click)

    def click_x_by_resourceId(self, location, x=0):
        '''
        点击UI元素
        :param location:
        :param value:
        :param x:
        :return:
        '''
        element = self.wait_until_element_found_by_resourceId(param=location)[x]  # 定位到元素
        element.click()

    def click_text_by_resourceId(self, location, text):
        '''
        点击UI元素
        :param location:
        :param value:
        :param x:
        :return:
        '''
        element = self.wait_until_element_found_by_resourceId(param=location)  # 定位到元素
        element.click()

    def press_back(self):
        '''
        返回
        :return:
        '''
        self.driver.press('back')

    def press_home(self):
        '''
        返回主页
        :return:
        '''
        self.driver.press('home')

    def exist_by_resourceId(self, param, timeout=30.0, retry_interval=2, wait_after_found=0.0):
        """
        定位元素，如果不存在就间隔若干秒后重试，直到元素定位成功或超时
        :param param: xpath字符串 或 元素对象
        :param timeout: 超时, 默认30秒
        :param retry_interval: 间隔时间, 默认2秒
        :param wait_after_found: 找到元素后，原地等待时间
        :return:
        """
        element = self.driver(resourceId=param) if isinstance(param, str) else param
        max_time = time() + timeout
        while True:
            try:
                assert element.exists
                if wait_after_found:
                    print("Element found，then sleep {} seconds".format(wait_after_found))
                sleep(wait_after_found)
                return element
            except AssertionError:
                param = param if isinstance(param, str) else param.selector
                print("Element 【 {} 】 Not found, Retry...".format(param))
                if time() > max_time > 0:
                    return None
                sleep(retry_interval)

    def wait_until_element_found_by_resourceId_text(self, param, text, timeout=30.0, retry_interval=2,
                                                    wait_after_found=0.0):
        """
        定位元素，如果不存在就间隔若干秒后重试，直到元素定位成功或超时
        :param param: xpath字符串 或 元素对象
        :param timeout: 超时, 默认30秒
        :param retry_interval: 间隔时间, 默认2秒
        :param wait_after_found: 找到元素后，原地等待时间
        :return:
        """
        element = self.driver(resourceId=param, text=text)
        max_time = time() + timeout
        while True:
            try:
                assert element.exists
                # if wait_after_found:
                # print("Element found，then sleep {} seconds".format(wait_after_found))
                sleep(wait_after_found)
                return element
            except AssertionError:
                param = param if isinstance(param, str) else param.selector
                # print("Element 【 {} 】 Not found, Retry...".format(param))
                if time() > max_time > 0:
                    raise AssertionError("Element 【 {} 】 located failed after {} timeout".format(param, timeout))
                sleep(retry_interval)

    def getPicture(self, fileName='./test.png'):
        '''
        获取截图
        :return:
        '''
        self.driver.screenshot(fileName)


if __name__ == '__main__':
    # device = '74a75bdd'
    device = 'TFBE10C14000077'
    b = Base(device)
    b.getPicture(fileName='./test.png')

    # b.getPicture(fileName='./test.jpg')
    # ele = b.wait_until_element_found_by_resourceId_text(param="com.iflytek.ainote.settings:id/title", text="WLAN",
    #                                                wait_after_found=0.5)
    # ele.click()
    # b.driver.press('home')
    # b.click_x_by_resourceId('com.toycloud.launcher:id/iv_settings')
    # b.adb_screen_shot()
    # print(b.driver,type(b.driver))
    # bp.back(2)
    # bp.d.screen_on()
    # sleep(1)
    # b.up(times=2)
    # b.start_app()
    # bp.d.screen_off()
