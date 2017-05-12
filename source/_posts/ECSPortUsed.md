---
title: Windows端口被占用
categories:
  - IT
tags:
  - IT
comments: false
date: 2017-04-26 13:08:08
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

> Windows 443 商品被占用处理

## 查看占用进程PID

在DOS中运行 `netstat -ano|findstr "443"` 查看

## 结束进程

### taskkill

使用 `taskkill`，DOS中执行 `taskkill /PID xx` 

### 任务管理器

打开`任务管理器`，查看中选择`PID`，然后在`进程`中结束

### system进程占用
停止 `Routing and Remote Access` 服务，完事儿后记得启动