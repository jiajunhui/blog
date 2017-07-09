---
title: Mac平台MySQL基础
categories:
  - IT
tags:
  - MySQL
comments: false
date: 2017-07-09 13:07:34
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

## 安装

Mac平台上MySQL支持`dmg`文件安装，打开[下载界面](https://dev.mysql.com/downloads/mysql/)

## 删除

停止MySQL，然后终端执行：

	sudo rm /usr/local/mysql
	sudo rm -rf /usr/local/mysql*
	sudo rm -rf /Library/StartupItems/MySQLCOM
	sudo rm -rf /Library/PreferencePanes/My*
	sudo rm -rf /Library/Receipts/mysql*
	rm -rf ~/Library/PreferencePanes/My*
	sudo rm -rf /Library/Receipts/MySQL*
	sudo rm -rf /var/db/receipts/com.mysql.*
	
编辑 `/etc/hostconfig` 文件，删除 `MYSQLCOM=-YES-`

## 重置root用户密码

> 可参考[官方做法](https://dev.mysql.com/doc/refman/5.7/en/resetting-permissions.html)，也可使用我这种**不安全**的做法

<!-- more -->

### 停止MySQL服务
	
`$ sudo /usr/local/mysql/support-files/mysql.server stop`
	
如果报错`ERROR! MySQL server PID file could not be found!`，则需要打开`系统偏好设置`——`MySQL`点击`Stop MySQL Server`
	
注：
	
* 使用 `mysql.server` 启动的，必须使用 `mysql.server` 停止
* 使用 `MySQL面板（系统偏好设置中）` 启动的，必须使用 `MySQL面板` 停止
* 两者都不能停止，可尝试`top`查看`PID`，然后使用`sudo kill PID`（**慎用**）

### 安全模式启动MySQL

`$ sudo /usr/local/mysql/bin/mysqld_safe --skip-grant-tables`

* --skip-grant-tables 不校验用户密码，任何存在的账户都可免密码登录，**极不安全**

### root账户进入MySQL

打开一个新终端，提示输入密码时按`回车`继续：

`$ /usr/local/mysql/bin/mysql -u root -p`

用户信息存在 `mysql.user`表中，需要先选择 `mysql` 这个数据库

	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 46
	Server version: 5.7.18
	
	Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.
	
	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.
	
	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
	
	mysql> use mysql;


### 重置root密码

直接更新 `mysql.user` 表中 `root` 用户的密码：

`mysql> UPDATE user SET authentication_string = PASSWORD('新密码') WHERE User='root';`

### 刷新权限

`mysql> flush privileges;`

### 重启MySQL

先停止、再启动，结束`安全启动MySQL`的终端。

## 数据库管理工具

推荐使用 [Navite for MySQL](https://www.navicat.com.cn/download)，也可使用官方的[MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

