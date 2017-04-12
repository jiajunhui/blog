---
title: ipa打包、上传至fir.im
categories:
  - IT
tags:
  - iOS
date: 2017-04-08 19:36:53
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

## 安装 fir-cli

参考官方文档：[https://github.com/FIRHQ/fir-cli/blob/master/doc/install.md](https://github.com/FIRHQ/fir-cli/blob/master/doc/install.md)

fir-cli 使用 Ruby 构建, 无需编译, 只要安装相应 gem 即可.

	$ ruby -v
	$ gem install fir-cli
	
### 安装错误

* 出现 `You don't have write permissions` ：

		Fetching: thor-0.19.4.gem (100%)
		ERROR:  While executing gem ... (Gem::FilePermissionError)
		    You don't have write permissions for the /Library/Ruby/Gems/2.0.0 directory.
		    
	解决：在命令前加上 `sudo`
	
<!-- more -->

* 出现 `Errno::EPERM`：

		ERROR:  While executing gem ... (Errno::EPERM)
		    Operation not permitted - /usr/bin/thor
	解决：重写 Ruby Gem 的 bindir, 执行 `echo 'gem: --bindir /usr/local/bin' >> ~/.gemrc`
	
* 其它错误参考官方文档

## 编译打包ipa文件

参考官方文档：[https://github.com/FIRHQ/fir-cli/blob/master/doc/build_ipa.md](https://github.com/FIRHQ/fir-cli/blob/master/doc/build_ipa.md)

用 CocoaPods 做依赖管理，打包使用 

`fir build_ipa path/to/workspace -w -S <scheme name>`

* 其它方法参考官方文档，也可使用Apple 官方的`xcodebuild`命令操作，查看文章[ipa打包、上传至pgyer.com](./AutomaticDeploymentToPgyer.html)

## 上传(发布)

参考官方文档：[https://github.com/FIRHQ/fir-cli/blob/master/doc/publish.md](https://github.com/FIRHQ/fir-cli/blob/master/doc/publish.md) 

## Python 自动部署

> 脚本集成实现打包、上传、发邮件通知功能，注意阅读**使用说明**
> 
> 以下代码有用拿走，有优化请 [**反馈**](mailto:hertz@hertzwang.com)


	# -*- coding: utf-8 -*-
	import os
	import re
	import sys
	import time
	import hashlib
	import string
	from email import encoders
	from email.header import Header
	from email.mime.text import MIMEText
	from email.utils import parseaddr, formataddr
	import smtplib
	
	# 使用说明：
	## 0.修改开发人员名称和测试人员名称，会在邮件中使用
	## 1.将该文件放置工程根目录（与.xcworkspace同级）
	## 2.修改以下相关信息：项目名称、scheme名称、fir token和email相关
	## 3.build 版本号必需是四段，否则查不出来（也可修改正则）
	
	# 项目相关设置
	## 开发人员
	dev_name = '-'
	## 测试人员
	tester_name = '-'
	## 项目名称
	project_name = "-"
	## 项目根目录,结尾不带 "/"，目前使用的是相对路径（可不修改）
	project_path = "."
	## scheme名称（终端进入工程根目录，执行 xcodebuild -list）
	scheme_name = "-"
	## App 名称（邮件中使用）
	app_name = "-"
	
	# fir token
	fir_api_token = "-"
	
	# email
	## 发件人邮箱账号
	from_addr = "-"
	## 发件人邮箱密码
	password = "-"
	## 邮箱服务地址，使用 smtp
	smtp_server = "smtp.-"
	## 收件人，多个用","分开
	to_addr = '-'
	
	# 执行返回结果
	result_not_exist = 256
	result_not_found = "Not found"
	
	# 打包ipa
	def build_ipa():
	    global ipa_filename
	    # ipa包名，之后会重命名
	    ipa_filename = "%s" % (project_name)
	    print('building...')
	    os.system ('/usr/local/bin/fir build_ipa %s -w -S %s -n %s' % (project_path,scheme_name,ipa_filename))
	    # 获取build版本
	    get_build_version()
	    # ipa包重命名
	    ipa_filename = "%siPhone%s版本" % (app_name, build_version)
	    os.system ('mv %s/fir_build/%s.ipa %s/fir_build/%s.ipa' % (project_path,project_name,project_path,ipa_filename))
	
	# 上传至 fir.im
	def upload_fir():
	    filePath = "%s/fir_build/%s.ipa" % (project_path, ipa_filename)
	    print('filePath:%s' % filePath)
	    if os.path.exists(filePath):
	        print('uploading...')
	        # 直接使用fir 有问题 这里使用了绝对地址 在终端通过 which fir 获得
	        cmd = "/usr/local/bin/fir publish '%s' -T '%s'" % (filePath,fir_api_token)
	        # 获取终端打印信息
	        cmdlog = execCmd(cmd)
	        # 过滤信息，查找短连接
	        ret = get_short_link(cmdlog)
	        return ret
	    else:
	        print("没有找到ipa文件")
	        return result_not_found
	
	# execute command, and return the output
	def execCmd(cmd):
	    r = os.popen(cmd)
	    text = r.read()
	    r.close()
	    return text
	
	
	def _format_addr(s):
	    name, addr = parseaddr(s)
	    return formataddr((Header(name, 'utf-8').encode(), addr))
	
	
	# 发邮件
	def send_mail(short_link):
	    
	    # 邮件内容
	    msg = MIMEText('Hi:\n    %siPhone%s版本已经打包完毕，请前往%s下载测试！' % (app_name, build_version, short_link), 'plain', 'utf-8')
	    # 邮件标题
	    msg['Subject'] = Header('%siPhone%s版打包程序' % (app_name,build_version), 'utf-8').encode()
	    # 发件人
	    msg['From'] = _format_addr('开发人员（%s）<%s>' % (dev_name,from_addr))
	    # 收件人
	    msg['To'] = _format_addr('测试人员（%s）<%s>' % (tester_name,to_addr))
	    # 其它设置
	    server = smtplib.SMTP(smtp_server, 25)
	    server.set_debuglevel(1)
	    server.login(from_addr, password)
	    server.sendmail(from_addr, string.splitfields(to_addr, ","), msg.as_string())
	    server.quit()
	
	# 获取短连接
	def get_short_link(text):
	    urls = re.findall(r"http://fir.im/+\w+", text)
	    if len(urls) > 0:
	        print(urls)
	        return urls[0]
	    else:
	        print(result_not_found)
	        return result_not_found
	
	# 获取build版本号：使用正则
	def get_build_version():
	    global build_version
	    # 查询build版本, fir_build 文件夹是 fir 打包生成的
	    cmd = "fir i ./fir_build/%s.ipa" % (project_name)
	    cmdlog = execCmd(cmd)
	    print('cmdlog:%s' % cmdlog)
	    regex = re.compile(r"\d+\.\d+\.\d+\.\d")
	    build_version = regex.findall(cmdlog)[0]
	
	def main():
	    begin_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	    # 使用fir-cli打包ipa
	    build_ipa()
	    # 上传fir
	    short_link = upload_fir()
	    # 发邮件
	    if short_link > result_not_found:
	        send_mail(short_link)
	    end_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	    print ('开始时间：%s \n结束时间：%s' % (begin_time,end_time))
	
	# 执行
	main()