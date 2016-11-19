# blog
### 搭建编写环境与源码同步

摘自[Hexo.io](https://hexo.io/docs/index.html)	

1.下载 [Node.js](https://nodejs.org)	 

2.下载 [Git](https://git-scm.com)	
	
3.下载MarkDown编辑工具：	
```Windows:```[MarkdownPad for Windows](http://markdownpad.com/)	
```Mac:```[MacDown](http://macdown.uranusjr.com/) 只支持Mac系统，下载不了时用[百度云盘](http://pan.baidu.com/s/1cuqThs)
			
4.终端/Dos 执行 ```$ npm install -g hexo-cli``` 安装Hexo 	

5.创建项目(blog为项目名)	

	$ hexo init blog	
	$ cd blog	
	$ npm install	

6.下载主题（摘自[Github](https://github.com/tufu9441/maupassant-hexo)）
	
	$ git clone https://github.com/tufu9441/maupassant-hexo.git themes/maupassant
	$ npm install hexo-renderer-jade --save
	$ npm install hexo-renderer-sass --save

注：执行时最好加```sudo```，执行```hexo-renderer-sass --save``` 应该会报错，解决可参照[中文文档](https://www.haomwei.com/technology/maupassant-hexo.html)
		
7.安装部署Support，本人部署在`github.io`上，选择`hexo-deployer-git`,也可使用[其它方式](https://hexo.io/zh-cn/docs/deployment.html)

```$ npm install hexo-deployer-git --save```


8.替换配置文字和文档	
	
```.../blog/_config.yml```	
```.../blog/source/*```		
```.../blog/themes/maupassant/_config.yml```
