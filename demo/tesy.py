#!/usr/bin/env python
# coding:utf-8
# @Time    : 2021/2/21 10:23 下午
# @Author  : 孔令超
# @File    : tesy.py
# @Software: PyCharm
import module
class Solutions():
    def shuixianhua(self,num):
        low = num % 10
        mid = num // 10 % 10
        high = num // 100
        if num == low ** 3 + mid ** 3 + high ** 3:
            return(num)
a=Solutions()
b=a.shuixianhua(153)
print(b)

foo()