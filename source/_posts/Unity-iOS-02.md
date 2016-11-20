---
title: Unity与iOS原生02
date: 2016-08-10 15:25:59
categories:
- iOS
tags: 
- Unity
- iOS
- Objective-C
---

# Unity调用iOS方法

**参考文章:[如何通过unity调用ios原生代码](http://dev.arinchina.com/unity3dwz/ar966/966/1)** ，不吝赐教[hertz@hertzwang.com](mailto:hertz@hertzwang.com)

### 一、Unity部分		


1.在Unity工程中新建一个`Assets`:

![新建一个Assets](../../../../images/20160810-unity-01.png "新建一个Assets")	

<!-- more -->

2.将`Square`拖动至`Hierarchy`:

![将Square拖动至Hierarchy](../../../../images/20160810-unity-02.png "将Square拖动至Hierarchy")	

3.给`Square`添加一个脚本，输入名字`UnitySendMessageToiOS`，语言使用默认的 `C Sharp`：

![给Square添加一个脚本](../../../../images/20160810-unity-03.png "给Square添加一个脚本")	

4.打开`UnitySendMessageToiOS`脚本添加按钮及点击事件：			

```
using UnityEngine;
using System.Collections;
using System.Runtime.InteropServices; //1.添加InteropServices

public class UnitySendMessageToiOS : MonoBehaviour {

	//2.声名外部方法（iOS方法）
	[DllImport("__Internal")] //注意没有分号
	extern static public void unitySendMessageWithString( string str );
	//more...


	// Use this for initialization
	void Start () {
		print ( "UnitySendMessageToiOS start" );
	}

	// Update is called once per frame
	void Update () {

	}

	//3.添加一个按钮调用外部方法
	void OnGUI () {
		if ( GUI.Button( new Rect( Screen.width - 200, 0, 200, 100 ), "Back" )) {
			print ( "Unity Button Clicked" ); //控制台打印

			unitySendMessageWithString ( "Unity Button Clicked" ); //调用外部方法
		}
	}
}
```


5.生成Xcode工程

### 二、iOS部分

1.在`UnityAppController.mm`里声名并实现外部方法`unitySendMessageWithString `：

```
extern "C" {
    void unitySendMessageWithString(char *message) {
        NSString *msg = [[NSString alloc] initWithCString:message encoding:NSUTF8StringEncoding];
        [[[UIAlertView alloc] initWithTitle:@"Alert" message:msg delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil, nil] show];
    }
}
```

2.修改`Bundle Identifier`用真机运行



