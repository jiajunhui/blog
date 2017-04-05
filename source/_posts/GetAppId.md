---
title: 获取App Id 和 URL Schemes
categories:
  - IT
  - iOS
tags:
  - iOS
date: 2017-04-02 16:51:20
---

> 由于工作需要应用跳转到其它App，那么问题来，怎么知道目标应用的App Id 和 URL Schemes 呢 ？

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢


# App Id

1. 打开 `iTunes`，在 **iTunes Store** 中搜索目标应用；
2. 在搜索结果中点击`v`按钮，选择**复制链接**；

		https://itunes.apple.com/cn/app/%E7%88%B1%E7%9C%8B%E5%84%BF%E7%AB%A5%E4%B9%90%E5%9B%AD/id480099078?mt=8
	
3. `.../id480099078?mt=8`中的 `480099078`就是目标应用的App Id.

# URL Schemes

## 拿到ipa

* 通过 iTunes 下载应用
* 通过助手下载应用
	* PP助手
	* 爱思助手
	* 91助手
	* 等......

## 查看 URL Schemes

> 其思路是通过应用 `Info.plist` 中的 `URL types`设置，来分析该应用的 URL Schemes
	
<!-- more -->

1. 解压ipa包(生成同名的文件夹)
	* 选中ipa包，右角打开方式选择**归档实用工具**
	* 将ipa包扩展名改为 `.zip`，然后双击


2. 显示包内容

	打开 *同名文件夹/Payload*，选中应用程序-->右键-->显示包内容

3. 查看 URL Schemes

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