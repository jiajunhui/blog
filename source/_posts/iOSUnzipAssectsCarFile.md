---
title: 解压Assects.car文件
categories:
  - IT
  - iOS
tags:
  - iOS
comments: false
date: 2017-06-29 14:40:49
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

> 前言：解压`ipa`并显示包内容后，看到一个 `Assets.car` 文件，心想它就是 `Assets.xcassets`

参考原文：[iOS学习之解压Assets.car](http://www.jianshu.com/p/a5dd75102467)

## 获取工具

1. 从[Github](https://github.com/steventroughtonsmith/cartool)下载工程；
2. 打开工程；
3. 编译后 Products 文件夹中得到 `cartool`

## 解压

	$ ./cartool /xxx/Assets.car /xxx/outputDirectory

* cartool: 命令行工具
* Assets.car: Assets.xcassets 压缩后的文件
* outputDirectory: 目标文件夹，必需存在！

## 脚本操作

<!-- more -->

> Pythone 脚本如下
> 
> 需要 `cartool工具`、`.car文件`和`脚本`在同一目录


	# -*- coding: utf-8 -*-
	import os
	
	# 工具目录
	cartool_path = "./"
	# 文件路径
	file_path = "./Assets.car"
	# 输出目录
	out_directory = "./outDirectory"
	
	def main():
	    # 定位
	    os.system('cd %s' % cartool_path)
	    # 判断输出目录是否存在，不存在则新建
	    if os.path.exists(out_directory) == False:
	        os.system('mkdir %s' % out_directory)
	    # 解压文件
	    os.system('%scartool %s %s' % (cartool_path,file_path,out_directory))
	    # 打开输出目录
	    os.system('open %s' % out_directory)
	
	main()

