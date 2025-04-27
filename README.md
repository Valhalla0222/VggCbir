# 使用VGGNET16实现以图搜图-CBIR
## 项目结构
~~~bash
--/dataset          		#数据集存放目录
 --/101_ObjectCategories	#第一个数据集
  --/accordion				#第一个数据集的一个类别
   --image_0001.jpg			#第一个数据集下第一个类别的第一张图片
 ...
 --/256_ObjectCategories	#第二个数据集
  --/001.ak47				#第二个数据集的一个类别
   --001_0001.jpg			#第二个数据集下第一个类别的第一张图片
 ...
--/icon						#存放界面图标的目录
 --author.png				#目录下的一个图标
 ...
--/test_set					#用于测试的图像集
 --/external				#存放的是数据集外的图像，主要为百度搜集
  --1.jpg					
  ...
 --/inside					#存放的是数据集内的图像
  --1.jpg
  ...
--app.py					#程序入口文件
--getFeatures.py			#提取数据集所有VGG图像特征
--search.py					#用于搜索的处理文件
--SelectAndSearch.py		#选择图像并进行搜索的文件
--VGGNET.py					#VGG的类文件，用于构造VGG模型并进行特征提取
--index.h5					#存放提取到的所有特征及其关系
--README.md					#项目说明文件
--requirements.txt			#项目依赖说明文件，可执行此文件下载项目所需要的包
~~~


