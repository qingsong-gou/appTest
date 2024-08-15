import subprocess
import time
import os
import sys


class Event(object):

    def __init__(self, device=""):
        if not (device == ""):
            self.device = device  # 指定设备
        else:
            self.device = self._gain_device()  # 本地设备

    def _gain_device(self):
        result2 = os.popen('adb devices ').readlines()
        device = result2[1]
        deviceName = ''
        if 'offline' in device:
            deviceName = device.split('offline')[0].rstrip('\t')
        if "device" in device:
            deviceName = device.split('device')[0].rstrip('\t')
        return deviceName

    def get_root_path(self):
        '''
        获取根目录
        :return:
        '''
        pre_path = sys.path[0]
        pre_path_split = pre_path.split("\\")
        count = 0
        for spath in pre_path_split:
            if spath == "InkScreen":
                break
            count += 1
        pre_path_new = ""
        for i in range(0, count + 1):
            pre_path_new = pre_path_new + pre_path_split[i] + "\\"
        return pre_path_new

    ################################event操作点击方法##############################################
    def virtual_key(self,
                    kind: str = "home or delete or up or down or volume_up or volume_down or volume_mute or power or back"):
        '''
        常用虚拟按键
        :param kind:
        :return: 
        '''
        if kind == "home":
            self.driver.press("home")  # 点击home键
        elif kind == "delete":
            self.driver.press("delete")  # 点击删除键
        elif kind == "up":
            self.driver.press("up")  # 点击上键
        elif kind == "down":
            self.driver.press("down")  # 点击下键
        elif kind == "volume_up":
            self.driver.press("volume_up")  # 点击音量+
        elif kind == "volume_down":
            self.driver.press("volume_down")  # 点击音量-
        elif kind == "volume_mute":
            self.driver.press("volume_mute")  # 点击静音
        elif kind == "power":
            self.driver.press("power")  # 点击电源键
        elif kind == "back":
            self.driver.press("back")  # 点击返回键
        raise Exception("输入kind有误")


if __name__ == "__main__":
    ev = Event()

    print(Event()._gain_device())
    # print(Event().get_root_path())
