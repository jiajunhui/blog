---
title: Unity与iOS原生03
categories:
- iOS
tags: 
- Unity
- iOS
- Objective-C
comments: false
date: 2017-06-29 15:56:42
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢



> 前言：本文章主要解决在现有iOS工程中集成多个Unity工程的问题
> 
> Unity 5.3.5f1  
> 
> Xcode 8.2.1
> 

# iOS原生集成多个Unity工程

## 知识点
1. Unity3d场景生成、上传、下载和加载（卸载未研究，必要时需卸载）；
2. Unity3d导出资源、加载资源、场景切换；
3. iOS原生集成Unity3d工程（集成Unity3d生成Xcode中的资源，参考[链接](http://qingqinghebiancao.github.io/2016/09/07/Unity集成到iOS本地工程中/)）
5. iOS原生与Unity3d交互（界面切换、数据交互）

## Unity部分

<!-- more -->

* 主工程(UnityMainProject)
	* 主场景(MainScene) *下载并加载服务器上的场景*
	* 其它场景(OtherScene)
* 场景工程(NewScene)
	* 场景(example)

## iOS原生部分

* 工程(UnitySceneDemo)


## Tips

###  Unity工程修改后重新生成Xcode工程，Libraries、Classes和Data需要更新

1. 移除 **Build Phases -> Compile Sources** 中 *路径为Class*下的 main.mm
2. 修改 **UnityAppController.h**

			// we will cache view controllers for fixed orientation
			// auto-rotation view contoller goes to index=0
		//	UnityViewControllerBase* _viewControllerForOrientation[5]; //TODO 未知后果
		    UIViewController* _viewControllerForOrientation[5];
		    
	和



		//inline UnityAppController*	GetAppController()
		//{
		//	return (UnityAppController*)[UIApplication sharedApplication].delegate;
		//}
		#import "AppDelegate.h"
		
		inline UnityAppController*  GetAppController()
		{
		    AppDelegate *delegate = (AppDelegate *)[UIApplication sharedApplication].delegate;
		    
		    return delegate.unityController;
		}
		
		
### Unity使用项目中场景需要设置：File -> Setting... 加入场景（所需要的）

# 合并多个Unity工程（场景包含多媒体）

## 操作步骤：
 
1. 导出资源：
 
	* 打开工程，选中`Project -> Assets`，右键并选择`Export Package...`，点击对话框右下角的`Export...`
 
2. 导入资源：

	* 方式一：打开工程，选择**菜单栏**的`Assets -> Import Package -> Custom Package...`，选择资源(**xx.unitypackage**)
	* 方式二：打开工程，双击***Finder***中的资源(**xx.unitypackage**)
	* 方式三：打开工程，从***Finder***中拖动到工程的*Assets*面板中

## 常见问题

0. 导入资源后文件夹目录混乱

	解决：
	* 方式一：手动拖动文件或文件夹到指定目录
	* 方式二：导出资源时外层加个文件夹

0. 场景切换报错（**S0**为场景名）
  
		Scene 'S0' (-1) couldn't be loaded because it has not been added to the build settings or the AssetBundle has not been loaded.
		To add a scene to the build settings use the menu File->Build Settings...
		UnityEngine.SceneManagement.SceneManager:LoadScene(String)
		ButtonClickedAction:LoadMathGameS0() (at Assets/Scripts/ButtonClickedAction.cs:62)
		UnityEngine.EventSystems.EventSystem:Update()
		
	该问题由未选择场景导致，解决操作如下：
	
	1. **Assets**中找到对应的场景（这里是*S0*）
	2. 选择**菜单栏**的`File -> Build Setting...`
	3. 将场景拖动到对话框的`Scenes In Build`中

0. 导入unitypackage后文件重复

		Assets/MathGame/Scripts/GameManager.cs(10,14): error CS0101: The namespace `global::' already contains a definition for `GameManager'
		Assets/MathGame/Scripts/SoundManager.cs(4,14): error CS0101: The namespace `global::' already contains a definition for `SoundManager'

	文件名冲突，解决：
	
	* 让提供者修改文件名和Class名

# 交互封装

## Unity调用原生

> 注：也可将第二部分内容合并到第四部分中，并将 **.m 改为 .mm** 即可

### 第一部分：Unity声名外部方法

> 这是 **C# JavaScript** ，也可使用 **JavaScript**

	using UnityEngine;
	using System.Collections;
	using UnityEngine.SceneManagement;
	using System.Runtime.InteropServices; //1.添加InteropServices
	
	public class ButtonClickedAction : MonoBehaviour {
	
		//2.声名外部方法（iOS方法）
		[DllImport("__Internal")] //注意没有分号
		extern static public void unitySendMessageShowNativeWindow( string str );
	
	
		// Use this for initialization
		void Start () {
			Debug.Log ("ButtonClickedAction Start");
		}
		
		......
		
### 第二部分：原生实现Unity声名的外部方法

> 必须在 `.mm` 文件中实现

	extern "C" {
	    void unitySendMessageShowNativeWindow(char *message) {
	        [[Unity_Bridge defaultInstance] unitySendMessageShowNativeWindow:message]; //获取单例，调用实例相应方法
	    }
	}
	
### 第三部分：封装

> **头文件 .h**

	#import <Foundation/Foundation.h>
	
	//MARK: - IKanUnityInterfaceDelegate
	/**
	 Unity bridge 协议方法
	 */
	@protocol IKanUnityInterfaceDelegate <NSObject>
	
	@optional
	
	
	/**
	 返回原生Window
	
	 @param message 当前场景名称
	 */
	- (void)unitySendMessageShowNativeWindow:(char *)message;
	
	@end
	
	
	
	//==============================================================
	
	//MARK: - @interface Unity_Bridge
	
	/**
	 Unity与原生的桥梁：实现Unity声名的方法
	 */
	@interface Unity_Bridge : NSObject<IKanUnityInterfaceDelegate>
	
	@property (nonatomic, assign) id<IKanUnityInterfaceDelegate> delegate; //委托
	
	
	/**
	 单例
	
	 @return 实例
	 */
	+ (instancetype)defaultInstance;
	
	//以下方法声名与协议中相同
	- (void)unitySendMessageShowNativeWindow:(char *)message;
	
	@end

> **实现 .m**

	#import "Unity-Bridge.h"
	
	@implementation Unity_Bridge
	
	+ (instancetype)defaultInstance {
	    static Unity_Bridge *instance = nil;
	    static dispatch_once_t onceToken;
	    dispatch_once(&onceToken, ^{
	        instance = [[Unity_Bridge alloc] init];
	    });
	    
	    return instance;
	}
	
	- (void)unitySendMessageShowNativeWindow:(char *)message {
	    if (_delegate && [_delegate respondsToSelector:@selector(unitySendMessageShowNativeWindow:)]) {
	        
	        [self.delegate unitySendMessageShowNativeWindow:message];
	    }
	}
	
	@end
	
### 第四部分：使用

	#import "ViewController.h"
	#import "Unity-Bridge.h"
	
	@interface ViewController ()<IKanUnityInterfaceDelegate>
	
	@property (nonatomic, strong) Unity_Bridge *unityBridge;
	
	@end
	
	@implementation ViewController
	
	- (void)dealloc
	{
	    _unityBridge.delegate = nil;
	}
	
	- (void)viewDidLoad {
	    [super viewDidLoad];
	    // Do any additional setup after loading the view, typically from a nib.
	    
	    _unityBridge = [Unity_Bridge defaultInstance];
	    _unityBridge.delegate = self;
	    
	}
	
	#pragma mark - Delegate
	
	- (void)unitySendMessageShowNativeWindow:(char *)message {
	    [(AppDelegate *)[UIApplication sharedApplication].delegate hideUnityWindow];
	
	    NSString *msg = [NSString stringWithUTF8String:message];
	    if ([msg isEqualToString:@"NewScene"]) {
	        [[IKanUnitySendMessage manager] sendMessage:"Main Camera" method:"ShowScene" msg:"MainScene"];
	    }
	}
	
	......
	
	@end
	

## 原生调用Unity

> 使用防御式编程将`UnitySendMessage`封装

### 基本封装

> **头文件 .h**

	#import <Foundation/Foundation.h>
	
	/**
	 原生调用Unity方法，防御式编程
	 */
	@interface IKanUnitySendMessage : NSObject
	
	/**
	 返回一个实例
	
	 @return 实例
	 */
	+ (nullable instancetype)manager;
	
	/**
	 调用Unity方法
	
	 @param obj Unity对象名
	 @param method 方法名
	 */
	- (void)sendMessage:(nonnull const char*)obj method:(nonnull const char*)method;
	
	/**
	 调用Unity方法
	 
	 @param obj Unity对象名
	 @param method 方法名
	 @param msg 参数
	 */
	- (void)sendMessage:(nonnull const char*)obj method:(nonnull const char*)method msg:(nullable const char*)msg;
	
	@end
	
	
> **实现 .m**

	#import "IKanUnitySendMessage.h"
	
	@implementation IKanUnitySendMessage
	
	+ (nullable instancetype)manager {
	    return [[IKanUnitySendMessage alloc] init];
	}
	
	- (void)sendMessage:(nonnull const char*)obj method:(nonnull const char*)method {
	    [self sendMessage:obj method:method msg:""];
	}
	
	- (void)sendMessage:(nonnull const char*)obj method:(nonnull const char*)method msg:(nullable const char*)msg {
	    
	    NSAssert(obj != nil && StrLength(obj) != 0, @"Unity Send Message obj 不能为nil 或 空");
	    NSAssert(method != nil && StrLength(method) != 0, @"Unity Send Message method 不能为nil 或 空");
	    
	    UnitySendMessage(obj, method, msg);
	}
	
	@end
	
	
