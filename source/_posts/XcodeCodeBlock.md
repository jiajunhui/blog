---
title: Xcode代码块提高开发效率
categories:
  - IT
tags:
  - Xcode
date: 2016-12-14 12:36:35
keywords: Xcode
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

*持续更新中...*	

前方：之前在视频中看到，敲几个字母就能生成大段代码，大大提高了效率，于是就开始研究实现。


### 代码块效果展示

使用Xcode开发时，在方法内输入 `if`会出现提示，如图：

![if代码块提示](./images/XcodeCodeBlock-if-01.png "if代码块提示")	
当然，这个是官方做的，输入 *回车* 后显示如图：

![if代码块显示](./images/XcodeCodeBlock-if-02.png "if代码块显示")

<!-- more -->

### 自定义块代码块

#### 编写代码块
	
以单例代码块为例，首先写一段代码：

	@implementation ViewController
	
	+ (instancetype)defaultInstance {
	    static <#Class#> *instance = nil;
	    static dispatch_once_t onceToken;
	    dispatch_once(&onceToken, ^{
	        instance = [[<#Class#> alloc] init];
	    });
	    
	    return instance;
	}
	
注： 使用 `<#` 和 `#>` 来实现提示

#### 存储代码块

1. 打开Xcode中代码块位置

	![Xcode中代码块位置](./images/XcodeCodeBlock-Code-Block-Position.png "Xcode中代码块位置")

2. 选中代码块，长按鼠标左键使光标变成黑色箭头，然后拖动至 **Xcode中代码块位置**

	![存储代码块](./images/XcodeCodeBlock-Code-Block-Move.png "存储代码块")

### 设置代码块

显示如图：

![设置代码块界面](./images/XcodeCodeBlock-Code-Block-Setting.png "设置代码块界面")

* Title 显示的标题
* Summary 概要描述信息
* Platform 平台，包括 All、iOS、macOS、tvOS、watchOS
* Language 语言，包括 Objective-C、Swift、Java、HTML 等
* **Completion Shortcut** 快捷键，输入的字符（如：`if`），一般加上前缀与系统的分开，我用的是 `hw`
* **Completion Scopes** 代码块作用域，只有在设置的域中可用

设置完成后就可以使用啦

### 编辑代码块

打开Xcode中代码块位置，选中需要编辑的代码块等上几秒（也可以双击），点击 `Edit` 开发编辑

### 删除代码块

打开Xcode中代码块位置，选中需要删除的代码块，按钮键盘上的 `delete` 键


### 代码块本地存放路径

存放路径 `~/Library/Developer/Xcode/UserData/CodeSnippets`，每一个`.codesnippet`文件都是一个代码块

### Objective-C 常用代码块

#### 声名

`@property (nonatomic, assign) <#Object#> <#name#>;`
`@property (nonatomic, strong) <#Object#> *<#name#>;`
`@property (nonatomic, copy) <#Object#> *<#name#>;`
`__weak typeof(self) weakSelf = self;`

	if (weakSelf) {
		typeof(self) strongSelf = weakSelf;
		    
		<#statements#>
	}

#### 单例

	+ (instancetype)defaultInstance {
	    static <#Class#> *instance = nil;
	    static dispatch_once_t onceToken;
	    dispatch_once(&onceToken, ^{
	        instance = [[<#Class#> alloc] init];
	    });
	    
#### 初始化UIWindow

    _window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    [_window setAutoresizesSubviews:NO];
    [_window makeKeyAndVisible];
    [_window setRootViewController:<#RootViewController#>];
    
#### Mark

`#pragma mark - <#Name#>`    
    
#### Unit Test

	/**
	 <#Description#>
	 */
	- (void)test<#Name#> {
	    
	    /* 使用预期：预期的作用在于执行网络请求后可等待请求返回结果 */
	    XCTestExpectation *expectation = [self expectationWithDescription:@"expectationWithDescription"]; //获取预期
	    
	    /* 执行网络请求代码，在 block 中执行 [expectation fulfill] 结束预期 */
	    <#执行网络请求代码#>
	    [expectation fulfill]; //结束预期
	    
	    /* 设置预期时长及预期失败处理 */
	    [self waitForExpectationsWithTimeout:10 handler:^(NSError * _Nullable error) {
	        if (error) {
	            //预期失败处理
	            NSLog(@"%@", error);
	        }
	    }];
	}

### Swift 常用代码块

#### Mark
`//MARK: - <#Name#> Protocol Method`

#### 类方法
	class func <#name#>(<#parameters#>) -> <#return type#> {
	        <#function body#>
	}
