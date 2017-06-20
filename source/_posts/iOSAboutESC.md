---
title: 关于转义、base64
categories:
  - IT
  - iOS
tags:
  - iOS
comments: false
date: 2017-06-20 22:19:37
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

> 前言：最近在搞一些东东，html中一堆堆的`%20`、`%3A`看着头大，然后硬着头皮去分析......

*持续更新中...*

## URL编码/解码

首先推荐一个网站：[站长工具-URL编码/解码](http://tool.chinaz.com/tools/urlencode.aspx)

Objective-C 中使用以下方法对URL编码、解码：


	// 编码
	- (nullable NSString *)stringByAddingPercentEncodingWithAllowedCharacters:(NSCharacterSet *)allowedCharacters NS_AVAILABLE(10_9, 7_0);
	
	// 解码 例：NSString *newStr = str.stringByRemovingPercentEncoding;
	@property (nullable, readonly, copy) NSString *stringByRemovingPercentEncoding NS_AVAILABLE(10_9, 7_0);
	


<!-- more -->

以下是非完全统计的转义（发现有误请联系）：

| 转义前 | 转义后 | 转义前 | 转义后 |
|--------|-------|--------|-------|
| %20 | 空格 | %21 | !  | 
| %22 | -  |  %23 | #  | 
| %25 | %  |  %26 | &amp; |
| %28 | (  |  %29 | )  | 
| %2B | +  |  %2C | ,  | 
| %2F | /  |  %3A | :  | 
| %3B | ;  |  %3C | &lt;  | 
| %3D | =  |  %3E | &gt;  | 
| %3F | ?  |  %40 | @  | 
| %5C | \  |  %7C | \|  | 

附：[HTML特殊转义字符对照表](http://tool.oschina.net/commons?type=2)

## 图片与base64

推荐文章：[关于图片的Base64编码，你了解吗？](http://www.toutiao.com/a6401965088865632514/)

### Objective-C 中使用（摘自：[iOS 图片转成base64编码](http://www.jianshu.com/p/91979b5def90)）：

* UIImage图片转成Base64字符串：

		UIImage *originImage = [UIImage imageNamed:@"originImage.png"];
		NSData *data = UIImageJPEGRepresentation(originImage, 1.0f);
		NSString *encodedImageStr = [data base64EncodedStringWithOptions:NSDataBase64Encoding64CharacterLineLength];
	
* Base64字符串转UIImage图片：

		NSData *decodedImageData = [[NSData alloc] 
		initWithBase64EncodedString:encodedImageStr options:NSDataBase64DecodingIgnoreUnknownCharacters];
		UIImage *decodedImage = [UIImage imageWithData:decodedImageData];


### 分析base64（个人理解，有其它见解请指教）

	data:image/jpg;base64,/9j/4Rbi.....GNWCdROn0HRe0dwb5G3CcC+C/pimS2dHAaQNXqft6//Z
	
* `data` 表示开始、`//Z` 表示结束
* `image` 内容类型
* `jpg` 图片类型
* `base64`内容开始标记
