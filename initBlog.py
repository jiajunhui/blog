# -*- coding: utf-8 -*-
import os
import sys


def main():
    # 新建tempBlog项目
    os.system ('hexo init tempBlog')
    # 复制tempBlog项目中的 node_modules 和 package.json 至Blog中
    os.system('mkdir node_modules')
    os.system ('cp -r ./tempBlog/node_modules/ ./node_modules/')
    os.system ('cp ./tempBlog/package.json ./')
    # 移除 tempBlog
    os.system('rm -rf tempBlog')
    # 执行安装
    os.system('npm install')
    # 安装部署Support
    os.system('npm install hexo-deployer-git --save')
    # 安装三方搜索
    os.system('npm install hexo-generator-searchdb --save')
    # 运行测试
    os.system('open -a Safari http://localhost:4000')
    os.system('hexo server')


main()
