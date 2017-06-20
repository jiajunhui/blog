---
title: iOS高精度计算
categories:
  - iOS
  - IT
tags:
  - iOS
comments: false
date: 2017-06-20 14:02:58
---

反馈请联系[**hertz@hertzwang.com**](mailto:hertz@hertzwang.com),谢谢

> 参考 
> 
> [iOS开发中高精度数值(货币)计算](http://blog.csdn.net/tqwei00001/article/details/53219404)
> 
> [iOS 中的数据结构和算法（一）：浮点数](http://chuansong.me/n/1560106) 


## 货币计算

使用 `@interface NSDecimalNumber : NSNumber`

成员方法：

* Adding 加法
* Subtracting 减法
* Multiplying 乘法
* Dividing 除法
* RaisingToPower 幂次方
* MultiplyingByPowerOf10 指数

## 高精度算法

<!-- more -->

摘自唐巧的总结：

* 浮点数在计算机内部并不是严格精确到每一位的。
* 在判断两个浮点数相等时，不能使用 == 操作符，需要通过比较两个浮点数差的绝对值，是否小于一个极小数的方式来判断。
* 如果你需要精确的浮点数计算，需要使用高精度算法。

提示：

1. 用两个数组来分别存放浮点数的整数部分和小数部分，数组中的每一个元素代表浮点数某一位的值；
2. 在计算两个浮点数的加法时，两个数组分别进行相加求和；
3. 需要处理进位和对齐，整数部分按低位对齐，小数部分按高位对齐。

算法代码，请指教：

	// 0.参与运算的数据
    NSString *numberA = @"555554.999999"; // 数据A
    NSString *numberB = @"111111.666667"; // 数据B
    
    // 1.分离整数部分和小数部分
    /// 1.1数据A
    NSMutableArray *numberAArray = [NSMutableArray new];
    for (NSString *number in [numberA componentsSeparatedByString:@"."]) {
        [numberAArray addObject:number];
    }
    /// 1.2数据B
    NSMutableArray *numberBArray = [NSMutableArray new];
    for (NSString *number in [numberB componentsSeparatedByString:@"."]) {
        [numberBArray addObject:number];
    }
    
    // 2.补0，整数部分补前面、小数部分补后面，使位数相等
    /// 2.1整数位补0
    long flag = [numberAArray[0] length] - [numberBArray[0] length];
    
    if (flag > 0) {
        for (int i = 0; i < flag; i++) {
            numberBArray[0] = [NSString stringWithFormat:@"0%@",numberBArray[0]];
        }
    } else if (flag < 0) {
        for (int i = 0; i < labs(flag); i++) {
            numberAArray[0] = [NSString stringWithFormat:@"0%@",numberAArray[0]];
        }
    }
    /// 2.2小数位补0
    flag = [numberAArray[1] length] - [numberBArray[1] length];
    
    if (flag > 0) {
        for (int i = 0; i < flag; i++) {
            numberBArray[1] = [NSString stringWithFormat:@"%@0",numberBArray[1]];
        }
    } else if (flag < 0) {
        for (int i = 0; i < labs(flag); i++) {
            numberAArray[1] = [NSString stringWithFormat:@"%@0",numberAArray[1]];
        }
    }
    
    // 3.分开相加，先小数部分、后整数部分
    /// 3.1小数位相加
    NSString *temp1A = numberAArray[1];
    NSString *temp1B = numberBArray[1];
    NSString *temp1 = @"";
    int add = 0;
    for (int i = 0; i < [temp1A length]; i++) {
        NSRange range = NSMakeRange([temp1A length]-i-1, 1);
        int tempA = [[temp1A substringWithRange:range] intValue];
        int tempB = [[temp1B substringWithRange:range] intValue];
        
        int sum = tempA + tempB + add;
        
        if (sum >= 10) {
            add = 1;
            sum -= 10;
        } else {
            add = 0;
        }
        
        temp1 = [NSString stringWithFormat:@"%d%@",sum, temp1];
    }
    /// 3.2整数位相加
    NSString *temp0A = numberAArray[0];
    NSString *temp0B = numberBArray[0];
    NSString *temp0 = @"";
    for (int i = 0; i < [temp0A length]; i++) {
        NSRange range = NSMakeRange([temp0A length]-i-1, 1);
        int tempA = [[temp0A substringWithRange:range] intValue];
        int tempB = [[temp0B substringWithRange:range] intValue];
        
        int sum = tempA + tempB + add;
        
        if (sum >= 10) {
            add = 1;
            sum -= 10;
        } else {
            add = 0;
        }
        
        temp0 = [NSString stringWithFormat:@"%d%@",sum, temp0];
    }

    // 4.打印结果
    NSLog(@"%@ + %@ = %@.%@", numberA, numberB, temp0, temp1);