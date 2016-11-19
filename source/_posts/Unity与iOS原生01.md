---
title: Unity与iOS原生01
date: 2016-08-09 10:08:11
tags: Unity与iOS原生
---

# 以原生为主的启动、原生与Unity3D视图Push/Pop切换

**参考文章:[在iOS APP中反复打开和关闭Unity页面](http://www.ceeger.com/forum/read.php?tid=20533)** ，不吝赐教[hertz@hertzwang.com](mailto:hertz@hertzwang.com)

[获取Unity](https://store.unity.com/cn)	

使用 `Unity Version 5.3.5f1 Personal`和`Xcode 7.3.1`
	
	
1、打开`Unity` New 一个新项目；		

2、`File`-->`Build Settings...`打开**Build Setting**对话框，`Platform`选择`iOS`，点击`Build`按钮生成`Xcode工程`；		

3、从`Finder`打开生成的`Xcode项目`；			

4、在`Project/Classes/`中新建原生视图`HomepageViewController`，使用XIB：	

4.1、`HomepageViewController.h`


```
#import <UIKit/UIKit.h>
	
/**
 *  定义推出Unity视图Block
 *
 *  @param isFirst 首次点击
 */
typedef void(^HomepageViewControllerPushUnityBlock)(BOOL isFirst);
	
/**
 *  原生主视图
 */
@interface HomepageViewController : UIViewController
	
/**
 *  按钮点击回调
 */
@property (nonatomic, copy) HomepageViewControllerPushUnityBlock homepageViewControllerPushUnityBlock;
	
@end
```
		

4.2、`HomepageViewController.m`	

```
/**
 *  Push Unity视图
 *
 *  @param sender 按钮
 */
- (IBAction)pushUnity:(UIButton *)sender {
    if (_homepageViewControllerPushUnityBlock) {
        _homepageViewControllerPushUnityBlock(!sender.isSelected);
    }
    
    [sender setSelected:YES];
}
```
	
	
5、在`UnityAppController.h`中声名`HomepageViewController`和`UINavigationController`：
	
	
```
HomepageViewController *homepageViewController; //原生主视图
UINavigationController *homepageNavigationController; //导航控制器
```

6、 `UnityAppController.mm`修改，调整**启动顺序**和**界面切效果**：

* 6.1、添加一个成员变量`homepageEnable`，用于防止多次创建原生视图	

		BOOL homepageEnable = YES; //只启动一次
* 6.2、修改方法`applicationDidBecomeActive:`，注释Unity的启动、添加调用新启动：	
		- (void)applicationDidBecomeActive:(UIApplication*)application
		{
			::printf("-> applicationDidBecomeActive()\n");
		
		    //add new code begin
		    if (homepageEnable) {
		        homepageEnable = NO;
		        [self performSelector:@selector(startHomepage:) withObject:application afterDelay:0];
		    }
		    //add new code end
		    
			if(_snapshotView)
			{
				[_snapshotView removeFromSuperview];
				_snapshotView = nil;
			}
		
			if(_unityAppReady)
			{
				if(UnityIsPaused() && _wasPausedExternal == false)
				{
					UnityPause(0);
					UnityWillResume();
				}
				UnitySetPlayerFocus(1);
			}
			else if(!_startUnityScheduled)
			{
				_startUnityScheduled = true;
				//[self performSelector:@selector(startUnity:) withObject:application afterDelay:0]; //注释Unity启动
			}
		
			_didResignActive = false;
		}	

	
* 6.3、实现`startHomepage:`方法：		

		/**
		 *  启动原生视图
		 *
		 *  @param application 应用
		 */
		- (void)startHomepage:(UIApplication*)application {
		    
		    //初始化原生视图
		    homepageViewController = [[HomepageViewController alloc] initWithNibName:@"HomepageViewController" bundle:[NSBundle mainBundle]];
		    __weak UnityAppController *weakSelf = self;
		    homepageViewController.homepageViewControllerPushUnityBlock = ^(BOOL isFirst) {
		        if (isFirst) {
		            [weakSelf startUnity:application]; //首次点击调用启动Unity
		        } else {
		            [weakSelf restartUnity];
		        }
		    };
		    //初始化导航控制器
		    homepageNavigationController = [[UINavigationController alloc] initWithRootViewController:homepageViewController];
			[homepageNavigationController setNavigationBarHidden:YES]; //隐藏导航栏
		    //设置为主视图
		    [_window setRootViewController:homepageNavigationController];
		    [UnityGetMainWindow() makeKeyAndVisible];
		} 

	

* 6.4、实现`restartUnity`方法：			

		/**
		 *  重启Unity
		 */
		- (void)restartUnity {
		    
		    [homepageNavigationController pushViewController:_rootController animated:YES]; //Push出Unity
		    
		    if (_didResignActive) {
		        UnityPause(false); //恢复Unity
		    }
		    
		    _didResignActive = NO;
		}
	
7、修改`UnityAppController+ViewHandling.mm`的`showGameUI`方法实现Push效果，并添加Pop按钮：		
```
- (void)showGameUI
{
	HideActivityIndicator();
	HideSplashScreen();
	
	// make sure that we start up with correctly created/inited rendering surface
	// NB: recreateGLESSurface won't go into rendering because _unityAppReady is false
	[_unityView recreateGLESSurface];
	
    //add code begin
    //添加一个按钮，用于返回原生视图
    UIButton *popToHomepageBtn = [UIButton buttonWithType:UIButtonTypeCustom];
    [popToHomepageBtn setFrame:CGRectMake(40, 84, 150, 44)];
    [popToHomepageBtn setBackgroundColor:[UIColor redColor]];
    [popToHomepageBtn setTitle:@"Pop to Homepage" forState:UIControlStateNormal];
    [popToHomepageBtn addTarget:self action:@selector(popToHomepageViewController) forControlEvents:UIControlEventTouchUpInside];
    [_rootView addSubview:popToHomepageBtn];
    //add code end
    
	// UI hierarchy
//	[_window addSubview: _rootView]; //注释window添加Unity主视图
//	_window.rootViewController = _rootController;//注释window添加Unity主视图
	[_window bringSubviewToFront:_rootView];
    [homepageNavigationController pushViewController:_rootController animated:YES]; //add code，Push Unity主视图
	
	// why we set level ready only now:
	// surface recreate will try to repaint if this var is set (poking unity to do it)
	// but this frame now is actually the first one we want to process/draw
	// so all the recreateSurface before now (triggered by reorientation) should simply change extents
	
	_unityAppReady = true;
	
	// why we skip present:
	// this will be the first frame to draw, so Start methods will be called
	// and we want to properly handle resolution request in Start (which might trigger surface recreate)
	// NB: we want to draw right after showing window, to avoid black frame creeping in
	
	_skipPresent = true;
	
	if (!UnityIsPaused())
		UnityRepaint();
	
	_skipPresent = false;
	[self repaint];
	
	[UIView setAnimationsEnabled:YES];
}
```

	
8、<a name="push-pop-crash"></a>修改`UnityAppController+ViewHandling.mm`的`transitionToViewController:`方法解决横屏下Push/Pop问题			

```
- (void)transitionToViewController:(UIViewController*)vc
{
    /**
     *  注释：只保留 layoutSubviews，
     *  
     *  willTransitionToViewController:fromViewController: 或 更新_rootController 导致Push后黑屏
     *  更换rootViewController导致不能Pop
     */
//	[self willTransitionToViewController:vc fromViewController:_rootController];
//	_rootController = vc;
//	_window.rootViewController = vc;

	[_rootView layoutSubviews];
}
```

	
### 总结
* 实现原生为主启动通过改变启动顺序实现
* 实现Push/Pop效果添加导航栏，并在相应的地方Push/Pop即可		

### 目前存在的问题（已解决，[参照8](#push-pop-crash)）
* 横屏状态Push，Unity界面黑屏
* 竖屏Push到Unity界面，Unity界面切换到横屏时点击Pop界面卡死

### 补充	
* 去掉Unity启动界面需要使用非个版的Unity，参考[官方说明-订阅详情-启动画面](https://store.unity.com/cn) 