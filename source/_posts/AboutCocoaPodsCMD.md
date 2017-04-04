---
title: CocoaPods周边
categories:
  - IT
tags:
  - iOS
date: 2017-04-04 20:45:51
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

*持续更新中......* 

## Ruby相关

0. 下载安装Ruby [https://www.ruby-lang.org/en/](https://www.ruby-lang.org/en/)
1. 升级Ruby环境 `$ sudo gem update --system`
2. 查看Ruby镜像 `$ gem sources -l`
3. 移除Ruby镜像 `$ gem sources --remove 镜像地址`
4. 添加Ruby镜像 `$ gem sources --add 镜像地址`

注：RubyGems 镜像参考[https://ruby.taobao.org/](https://ruby.taobao.org/)

<!-- more -->

## CocoaPods相关

0. 安装CocoaPods `$ sudo gem install cocoapods`
1. 卸载CocoaPods `$ sudo gem uninstall cocoapods`
2. 查询三方版本信息 `$ pod pod search 项目名`
2. 根据Podfile集成 `$ pod install`
3. Podfile 模板

		platform :ios, '8.0'
		use_frameworks!
		
		target 'MyApp' do
		  pod 'AFNetworking', '~> 3.0'
		end

注：参考 [https://guides.cocoapods.org](https://guides.cocoapods.org)

## 问题

### 升级 Mac OS 导致 `-bash: pod: command not found`

> 解决方案【转载：[解决升级EI Capiton CocoaPods "pod: command not found"](http://www.jianshu.com/p/6ff1903c3f11)】

1.为了安全起见，执行命令"sudo gem uninstall cocoapods"，卸载原有的CocoaPod
	
2.执行命令"sudo gem install -n /usr/local/bin cocoapods"来重新安装cocoapod
	
3.如果没有权限执行pod，执行命令"sudo chmod +rx /usr/local/bin/"，赋予/usr/local/bin给予执行与读取权限
	
参考链接：[https://github.com/CocoaPods/CocoaPods/issues/3736](https://github.com/CocoaPods/CocoaPods/issues/3736)