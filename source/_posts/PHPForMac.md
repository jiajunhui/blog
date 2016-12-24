---
title: PHP for Mac
categories:
  - IT
tags:
  - PHP
date: 2016-12-07 09:55:33
keywords: php for mac
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

前言：在Mac上运行PHP文件，因Mac自带Apache服务和PHP，只需简单配置即可运行静态PHP文件

### 两个文件夹路径

1. Apache 配置文件目录 `/etc/apache2`
2. 部署目录 `/Library/WebServer/Documents`

### 两个命令

1. 启动 Apache 服务 `sudo apachectl start`
2. 停止 Apache 服务 `sudo apachectl stop`

### 一个配置文件

修改 Apache 配置文件目录下的 `httpd.conf` ，将 `LoadModule php5_module libexec/apache2/libphp5.so` 打开（将前面的`#`去掉，修改需要 *root*权限）