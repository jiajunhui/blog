---
title: ipa打包、上传至pgyer.com
categories:
  - IT
tags:
  - iOS
date: 2017-04-12 08:35:32
---

> 实现ipa打包、上传 
> 环境：Mac OS 10.12、Xcode 8.3、Python 2.7.10
> 反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢


## 打包

### 使用官方的 `xcodebuild` 命令

> cd 到工程根目录（工程使用cocoapods管理）

1. 清空缓存 clean

		$ xcodebuild clean -workspace MyWorkspace.xcworkspace -scheme MyScheme
		
2. 归档 archive 
<!-- more -->

		$ xcodebuild archive -workspace MyWorkspace.xcworkspace -scheme MyScheme -archivePath ./build/MyWorkspace.xcarchive
		
	* `archive`：归档为 `.xcarchive`文件（*Archive a scheme from the build root (SYMROOT).  This requires specifying a scheme.*）
	
	* `-workspace`：当前目录下`.xcworkspace`文件路径（*Build the workspace name.xcworkspace*
	
	* `-scheme`：项目的`scheme`（*Build the scheme specified by schemename.  Required if building a workspace*），可执行`xcodebuild -list`查看	
	
	* `-archivePath`：归档后文件位置（*Specifies the path for the archive produced by the archive action, or specifies the archive that should be exported when -exportArchive is passed*）
           
3. 导出 ipa

		$ xcodebuild -exportArchive -archivePath ./build/MyWorkspace.xcarchive -exportPath ./build/ -exportOptionsPlist ./build/export.plist
		
	* `-exportArchive`：导出iad文件（*Specifies that an archive should be exported. Requires -archivePath, -exportPath, and -exportOptionsPlist.  Cannot be passed along with an action*）
	
	* `-archivePath`：同上
	
	* `-exportPath`：导出的路径（*Specifies the destination for the exported product, including the name of the exported file*），文件名默认为`MyWorkspace.ipa`

	* `-exportOptionsPlist`：指定一个`plist`文件（*Specifies options for -exportArchive.  xcodebuild -help can print the full set of available options*）

	* `export.plist`：**需要手动创建**，注意修改`teamID`。了解更多执行 `xcodebuild -help`查看 *Available keys for -exportOptionsPlist*
	
			<?xml version="1.0" encoding="UTF-8"?>
			<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
			<plist version="1.0">
				<dict>
					<key>method</key>
					<string>ad-hoc</string>
					<key>teamID</key>
					<string>10位字符，你的teamId</string>
				</dict>
			</plist>

### 使用三方的 `fir` 命令

准备：[安装fir-cli](https://github.com/FIRHQ/fir-cli/blob/master/doc/install.md)

	$ fir build_ipa path/to/workspace -w -S <scheme name>
	
执行完成后会生成`fir_build`文件夹，更多信息[参考官方说明](https://github.com/FIRHQ/fir-cli/blob/master/doc/build_ipa.md)


## 上传（发布）

> 将ipa包上传至pgyer.com，主要使用Web、[桌面客户端](https://www.pgyer.com/apps/)、[开放API](https://www.pgyer.com/doc/api#uploadApp)、[FastLane](https://www.pgyer.com/doc/view/fastlane)、[Xcode 插件](https://www.pgyer.com/doc/view/xcode_plugin)、[Jenkins](https://www.pgyer.com/doc/view/jenkins_ios)

### 使用一条命令快速上传应用


	curl -F "file=@{$filePath}" \
	-F "uKey={$uKey}" \
	-F "_api_key={$apiKey}" \
	https://www.pgyer.com/apiv1/app/upload


* ilePath：是应用安装包文件的路径
* uKey：是开发者的用户 Key，在应用管理-API中查看
* apiKey：是开发者的 API Key，在应用管理-API中查看


## Python 自动部署

> 脚本集成实现打包、上传、发邮件通知功能，注意阅读**使用说明**
> 
> 以下代码有用拿走，有优化请 [**反馈**](mailto:hertz@hertzwang.com)

使用`Python` 封装 `xcodebuild` 自动布置 pgyer.com，支持邮件通知

	# -*- coding: utf-8 -*-
	import os
	import re
	import sys
	import time
	import hashlib
	import string
	import json
	from email import encoders
	from email.header import Header
	from email.mime.text import MIMEText
	from email.mime.multipart  import MIMEMultipart
	from email.utils import parseaddr, formataddr
	import smtplib
	
	#  当前版本：v1.0.1
	#
	## 使用说明：
	## 0.修改开发人员名称、测试人员名称、App名称，会在邮件中使用
	## 1.将该文件放置工程根目录（与.xcworkspace同级）
	## 2.修改以下相关信息：项目名称、scheme名称、teamId、pgyer Info相关和email相关
	## 3.修改删除ipa标记
	
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
	## teamId
	team_id = "-"
	
	# pgyer Info
	api_key = "-"
	user_key = "-"
	
	# email
	## 发件人邮箱账号
	from_addr = "-"
	## 发件人邮箱密码
	password = "-"
	## 邮箱服务地址
	smtp_server = "-"
	## 收件人，多个用","分开
	to_addr = '-'
	
	# 删除ipa标记，默认为 False
	clear_ipa = False
	
	# 执行返回结果
	result_not_exist = 256
	result_not_found = "Not found"
	
	# 清空缓存
	def xcb_clean():
	    print ('clean...')
	    os.system('cd %s;xcodebuild clean -workspace %s/%s.xcworkspace -scheme %s' % (project_path,project_path,project_name,scheme_name))
	
	
	# 生成plist文件
	def generate_plist_file():
	    print ('generate export.plist')
	    plistText = """\
	        <?xml version="1.0" encoding="UTF-8"?>
	        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
	        <plist version="1.0">
	            <dict>
	                <key>method</key>
	                <string>ad-hoc</string>
	                <key>teamID</key>
	                <string>%s</string>
	            </dict>
	        </plist>
	        """ % (team_id)
	    plist = open("%s/build/export.plist" % project_path, "w")
	    plist.write(plistText)
	    plist.close()
	
	
	# 归档为.xcarchive格式
	def xcb_archive():
	    print ('archive...')
	    build_path = '%s/build' % project_path
	    if os.path.exists(build_path) == False:
	        os.system('mkdir %s' % build_path)
	    os.system('xcodebuild archive -workspace %s/%s.xcworkspace -scheme %s -archivePath %s/build/%s.xcarchive' % (project_path,project_name,scheme_name,project_path,project_name))
	    # 生成plist文件，用于打包
	    generate_plist_file()
	
	
	# 执行命令，并返回输出值
	def exec_cmd(cmd):
	    r = os.popen(cmd)
	    text = r.read()
	    r.close()
	    return text
	
	
	# 获取build版本号：使用正则
	def get_build_version():
	    print ('get build version...')
	    global build_version
	    # 通过Info.plist，查询build版本  # TODO 优化查询条件
	    cmd = "cat %s/%s/Info.plist" % (project_path,project_name)
	    cmdlog = exec_cmd(cmd)
	    regex = re.compile(r"\d+\.\d+\.\d+\.\d")
	    build_version = regex.findall(cmdlog)[0]
	
	
	# 导出ipa
	def xcb_exportArchive():
	    global ipa_filename
	    print ('exportArchive...')
	    print('它没有停止，只是需要时间，请稍等')
	    os.system('xcodebuild -exportArchive -archivePath %s/build/%s.xcarchive -exportPath %s/build/ -exportOptionsPlist %s/build/export.plist' % (project_path,project_name,project_path,project_path))
	    # 获取build版本号
	    get_build_version()
	    # ipa包重命名
	    ipa_filename = "%siPhone%s版本" % (app_name, build_version)
	    os.system('mv %s/build/%s.ipa %s/build/%s.ipa' % (project_path, project_name, project_path, ipa_filename))
	
	
	# 获取短连接
	def get_short_link(text):
	    print ('get short link')
	    global qrcode_url
	    global short_link
	    # 初始化 short_link
	    short_link = result_not_found
	    # json 解析上传返回结果
	    decodejson = json.loads(text)
	    shortcut_url = decodejson['data']['appShortcutUrl']
	    qrcode_url = decodejson['data']['appQRCodeURL']
	    qrcode_url = qrcode_url.encode('UTF-8')
	    if len(shortcut_url) > 0:
	        short_link = "http://www.pgyer.com/%s" % (shortcut_url.encode('UTF-8'))
	    else:
	        print(result_not_found)
	
	
	# 上传至 pgyer.com
	def upload_pgyer():
	    print ('pgyer upload')
	    filePath = "%s/build/%s.ipa" % (project_path, ipa_filename)
	    if os.path.exists(filePath):
	        print('uploading...')
	        # 使用curl命令上传
	        cmd = "curl -F 'file=@%s/build/%s.ipa' -F 'uKey=%s' -F '_api_key=%s' https://qiniu-storage.pgyer.com/apiv1/app/upload" % (project_path,ipa_filename,user_key,api_key)
	        # 获取终端打印信息
	        cmdlog = exec_cmd(cmd)
	        # 过滤信息，查找短连接
	        get_short_link(cmdlog)
	    else:
	        print("没有找到ipa文件")
	
	
	def _format_addr(s):
	    name, addr = parseaddr(s)
	    return formataddr((Header(name, 'utf-8').encode(), addr))
	
	# 发邮件
	def send_mail():
	    print ('send mail')
	    if short_link == result_not_found:
	        return
	    # 技术参考：https://docs.python.org/2/library/email-examples.html
	    msg = MIMEMultipart('alternative')
	    # 邮件标题
	    msg['Subject'] = Header('%siPhone%s版打包程序' % (app_name,build_version), 'utf-8').encode()
	    # 发件人
	    msg['From'] = _format_addr('开发人员（%s）<%s>' % (dev_name,from_addr))
	    # 收件人
	    msg['To'] = _format_addr('测试人员（%s）<%s>' % (tester_name,to_addr))
	    # 正文
	    # Create the body of the message (a plain-text and an HTML version).
	    html = """\
	        <html>
	          <head></head>
	          <body>
	            <p>Hi!<br>
	              &nbsp;&nbsp;&nbsp;&nbsp;%siPhone%s版本已经打包完毕，请前往<a href=%s>%s</a>下载测试！<br>
	              &nbsp;&nbsp;&nbsp;&nbsp;或扫描下方二维码：
	            </p>
	            &nbsp;&nbsp;&nbsp;&nbsp;<img src="%s">
	          </body>
	        </html>
	        """ % (app_name,build_version,short_link,short_link,qrcode_url)
	    # Record the MIME types of both parts - text/plain and text/html.
	    part = MIMEText(html, 'html', 'utf-8')
	
	    # Attach parts into message container.
	    # According to RFC 2046, the last part of a multipart message, in this case
	    # the HTML message, is best and preferred.
	    msg.attach(part)
	
	    # 其它设置
	    server = smtplib.SMTP(smtp_server, 25)
	    server.set_debuglevel(1)
	    server.login(from_addr, password)
	    server.sendmail(from_addr, string.splitfields(to_addr, ","), msg.as_string())
	    server.quit()
	
	
	# 清理归档文件
	def clear_archive_file():
	    print ('清理归档文件...')
	    os.system('rm -rf %s/build/*.xcarchive' % project_path)
	    if clear_ipa == True:
	        os.system('rm -rf %s/build/*.ipa' % project_path)
	
	
	def main():
	    begin_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	    # 清理缓存
	    xcb_clean()
	    # 归档为.xcarchive格式
	    xcb_archive()
	    # 导出ipa
	    xcb_exportArchive()
	    # 上传pgyer
	    upload_pgyer()
	    # 发邮件
	    send_mail()
	    # 清理归档文件
	    clear_archive_file()
	    end_time = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	    print ('开始时间：%s \n结束时间：%s' % (begin_time,end_time))
	
	
	# 执行
	main()
	
	
	# change log
	
	# 2017.04.11 v1.0.1
	# 新增删除 .xcarchive 和 ipa 文件功能，ipa 文件可通过设置 clear_ipa 标记来删除
	#
	# 2017.04.11 release v1.0










