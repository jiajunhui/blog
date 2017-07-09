---
title: Mac OS 上安装 Niginx
categories:
  - IT
tags:
  - Tools
comments: false
date: 2017-07-07 17:47:40
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

> 参考[Mac下用brew安装nginx](http://www.jianshu.com/p/6c7cb820a020)


## 安装brew(Homebrew)

一般默认装有`brew`

	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	
	
	
`brew`常用命令：

* 搜索软件：`brew search nginx`
* 卸载软件：`brew uninstall nginx`
* 升级brew：`sodu brew update`
* 查看安装信息：`sodu brew info nginx`
* 查看已经安装的软件：`brew list`
* 注：脚本会在执行前暂停，按下回车并输入管理员密码。更多信息[查看官方网站](https://brew.sh/index_zh-cn.html)

<!-- more -->

## 安装Nginx

	$ brew install nginx

`nginx`常用命令：

* 启动`nginx`服务：`sudo brew services start nginx`
* 关闭`nginx`服务：`sudo brew services stop nginx`
* 重新加载`nginx`：`nginx -s reload`
* 停止`nginx`：`nginx -s stop`
* 检查配置文件语法：`nginx -t`
	
注：也可使用`sudo nginx`启动、使用`sudo nginx -s stop`停止。

## Nginx相关信息

* 部署路径：`/usr/local/var/www`
* `nginx`配置文件路径：`/usr/local/etc/nginx/nginx.conf`
* 默认使用`8080`端口

执行 `brew info nginx` 后得到以下信息

	nginx: stable 1.12.0 (bottled), devel 1.13.2, HEAD
	HTTP(S) server and reverse proxy, and IMAP/POP3 proxy server
	https://nginx.org/
	/usr/local/Cellar/nginx/1.12.0_1 (23 files, 1MB) *
	  Poured from bottle on 2017-07-08 at 18:27:37
	From: https://github.com/Homebrew/homebrew-core/blob/master/Formula/nginx.rb
	==> Dependencies
	Required: pcre ✔, openssl@1.1 ✔
	Optional: passenger ✘
	==> Options
	--with-debug
		Compile with support for debug log
	--with-gunzip
		Compile with support for gunzip module
	--with-passenger
		Compile with support for Phusion Passenger module
	--with-webdav
		Compile with support for WebDAV module
	--devel
		Install development version 1.13.2
	--HEAD
		Install HEAD version
	==> Caveats
	Docroot is: /usr/local/var/www
	
	The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
	nginx can run without sudo.
	
	nginx will load all files in /usr/local/etc/nginx/servers/.
	
	To have launchd start nginx now and restart at login:
	  brew services start nginx
	Or, if you don't want/need a background service you can just run:
	  nginx
	  
	  
	  
	  
