---
title: PHP CodeIngiter 初探
categories:
  - IT
tags:
  - PHP
comments: false
date: 2017-07-09 09:51:38
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

> 主要摘自[CodeIgniter 中国 »  文档首页](http://codeigniter.org.cn/user_guide/index.html)

## 下载

[点击打开下载界面](http://codeigniter.org.cn/user_guide/installation/downloads.html)

## 安装说明

### 安装 CodeIgniter：

1. 解压缩安装包；
2. 将 CodeIgniter 文件夹及里面的文件上传到服务器，通常 index.php 文件将位于网站的根目录；
3. 使用文本编辑器打开 application/config/config.php 文件设置你网站的根 URL，如果你想使用加密或会话，在这里设置上你的加密密钥；
4. 如果你打算使用数据库，打开 application/config/database.php 文件设置数据库参数。

### 安全性

将 `system` 和 `application` 文件夹放置 Web 根目录之外，修改 *文件夹* 名称，并设置 `index.php` 中的 *`%system_path`* 和 *`$application_folder`*，最好设置成绝对路径。

生产环境要禁用 PHP 错误报告以及所有其他仅在开发环境使用的功能。在 CodeIgniter 中，可以通过设置 `ENVIRONMENT` 常量来做到这一点，这在 [安全](http://codeigniter.org.cn/user_guide/general/security.html) 这篇指南中有着更详细的介绍。
