# -*- coding: utf-8 -*-
"""
@Time ： 2023/8/11 10:32
@Auth ： qsgou
@File ：timeFormat.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import time


def get_local_time():
    tformat = '%Y_%m_%d_%H%M%S'
    mytime = time.strftime(tformat, time.localtime())
    return mytime


def get_local_date():
    tformat = '%Y %m %d %H:%M:%S'
    mytime = time.strftime(tformat, time.localtime())
    return mytime


if __name__ == '__main__':
    print(get_local_date())
