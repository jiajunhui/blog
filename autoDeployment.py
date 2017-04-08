# -*- coding: utf-8 -*-
import os
import sys


def main():
    # 清空缓存
    os.system ('hexo clean')
    # 生成
    os.system ('hexo g')
    # 发布
    os.system ('hexo d')

main()
