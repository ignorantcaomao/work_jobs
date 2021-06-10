#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/1 15:32
# @Author  : djs
# @FileName: __init__.py
# @Software: PyCharm

# 利用Event类模拟红绿灯
import threading
import time

event = threading.Event()


def lighter():
    green_time = 5  # 绿灯时间
    red_time = 5  # 红灯时间
    event.set()  # 初始设为绿灯
    while True:
        print("\33[32;0m 绿灯亮...\033[0m")
        time.sleep(green_time)
        event.clear()
        print("\33[31;0m 红灯亮...\033[0m")
        time.sleep(red_time)
        event.set()


def run(name):
    while True:
        if event.is_set():  # 判断当前是否"放行"状态
            print("一辆[%s] 呼啸开过..." % name)
            time.sleep(1)
        else:
            print("一辆[%s]开来，看到红灯，无奈的停下了..." % name)
            event.wait()
            print("[%s] 看到绿灯亮了，瞬间飞起....." % name)


if __name__ == '__main__':

    light = threading.Thread(target=lighter, )
    light.start()

    for name in ['奔驰', '宝马', '奥迪']:
        car = threading.Thread(target=run, args=(name,))
        car.start()
