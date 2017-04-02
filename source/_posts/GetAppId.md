---
title: 获取ipa中应用ID(URL Schemes)
categories:
  - IT
  - iOS
tags:
  - iOS
date: 2017-04-02 16:51:20
---

> 由于工作需要应用跳转到其它App，那么问题来，怎么知道目标应用的App Id呢 ？

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢


## 拿到ipa

* 通过 iTunes 下载应用
* 通过助手下载应用
	* PP助手
	* 爱思助手
	* 91助手
	* 等......

## 查看 App Id

> 其思路是通过应用 `Info.plist` 中的 `URL types`设置，来分析该应用的 App Id
	
<!-- more -->

1. 解压ipa包(生成同名的文件夹)
	* 选中ipa包，右角打开方式选择**归档实用工具**
	* 将ipa包扩展名改为 `.zip`，然后双击


2. 显示包内容

	打开 *同名文件夹/Payload*，选中应用程序-->右键-->显示包内容

3. 查看 App id

	打开文件夹中的 *Info.plist* 文件，搜索关键字 `schemes`，查看 `URL types` 各个 `item` 中的  `URL Schemes`
	
	* 同应用名或相似
	* 同 **Bundle identifier**或相似
	

## 进一步分析

> 有些在 Info.plist 中的不能直接看出来，进一步分析


* `Item`中没有`URL identifier`，有可能以 `wx`、`wb` 开头并加上字符、数字来假装成微信、微博之类，需要尝试
* 依次尝试 `URL Schemes`

注：prefs 是跳转到**设置**

## 束手无策

Info.plist中没有 `URL types`，这是个问题，[欢迎讨论](mailto:hertz@hertzwang.com)