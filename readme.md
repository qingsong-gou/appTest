1.安装环境
1.1安装依赖包
pip install -r requirements.txt
1.2安装allure插件
allure-commandline-2.21.0.zip
工具路径：https://svn.iflytek.com:8888/svn/CTI_FYJ/Trunk/Project/06.Test/测试工具/AI学APP相关工具
1.3安装chormedriver环境
针对自己chorme版本去下载driver到driver目录
http://chromedriver.storage.googleapis.com/index.html


用例书写：
1.在page目录创建页面类，其中包含页面元素的操作
2.在testCase目录创建对应的测模块文件名，需以test_开头，测试类需以Test开头，测试方法以test开头；logging.info可将日志输出至log目录，用例失败后自动截图会输出到pictures目录
3.用例执行可在当前文件中执行 pytest.main(['-vsq', './testCase/test_*.py']) 具体参数可参考 https://learning-pytest.readthedocs.io/zh/latest/
4.运行整个项目的测试用例需在 main.py中运行，其调用utils中的 压缩报告，上传服务器，发邮件等功能
5.日志，图片目录可删除，在运行用例后自动创建
