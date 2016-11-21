# blog
### 搭建编写环境与源码同步

#### 一、环境

摘自[Hexo.io](https://hexo.io/docs/index.html)	

1. 下载 [Node.js](https://nodejs.org)	 

2. 下载 [Git](https://git-scm.com)	
			
3. 终端/Dos 执行 ```$ npm install -g hexo-cli``` 安装Hexo 	
4. 下载MarkDown编辑工具：	
```Windows:```[MarkdownPad for Windows](http://markdownpad.com/)	
```Mac:```[MacDown](http://macdown.uranusjr.com/) 只支持Mac系统，下载不了时用[百度云盘](http://pan.baidu.com/s/1cuqThs)

5. 下载[GitHub Desktop](https://desktop.github.com)

#### 二、搭建项目

1. 使用 *GitHub Desktop* 下载该项目
2. 执行 `hexo init tempBlog` 创建临时项目
3. 获取**Hexo**相关资源，将 *tempBlog* 文件夹中非以下信息全复制到 *blog* 文件夹中后删除 *tempBlog* 文件夹：	

		.../tempBlog/_config.yml
		.../tempBlog/scaffolds/		
		.../tempBlog/source/	
		.../tempBlog/themes/
		
	
4. 进入 *blog* 文件夹，执行 `npm install` 命令
	
5. 安装部署Support，本人部署在`github.io`上，选择`hexo-deployer-git`,也可使用[其它方式](https://hexo.io/zh-cn/docs/deployment.html)

		$ npm install hexo-deployer-git --save

6. 安装搜索三方`hexo-generator-searchdb`

		$ npm install hexo-generator-searchdb --save
	
9. 部署

	方式一 执行`hexo generate --deploy` 
	
	方式二 执行`hexo deploy --generate` 
	
	方式三 执行 `hexo g` 执行 `hexo d`

### 常见问题
1. 部署后页面空白([参考](http://blog.csdn.net/xiangwanpeng/article/details/53155642))

	原因：**NexT** 的 *_config.yml* 中 *vendors* 模块配置冲突
	
		...
		vendors:
	  	# Internal path prefix. Please do not edit it.
		  _internal: vendors
		  ...


	
	解决：
	
	第一步：**NexT** 的 *_config.yml* 中 *vendors* 模块修改	
		
		...
		vendors:
	  	# Internal path prefix. Please do not edit it.
		  _internal: <#新名字#>
		  ...

	第二步： *.../themes/next/source/* 中的 **vendors** 改为 <#新名字#>
	
	第三步：执行 `hexo clean` 后部署，多刷新几次即可
