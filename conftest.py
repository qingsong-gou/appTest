import os
import logging
import subprocess
import pytest

import warnings
from utils.base import Base
from utils.event import Event
from utils.getRootPath import get_project_root
from utils.operationData import makeDir
from utils.timeFormat import get_local_time
from datetime import datetime
from py.xml import html

warnings.filterwarnings("ignore")  # 忽略 UserWarning
device = Event()._gain_device()
project_root = get_project_root()
driver = None


def makeLogDir(device, nameDir):
    """创建测试运行log文件，供Text控件实时读取,运行在主进程"""
    log_path = makeDir(dirName=nameDir)
    log_file_name = os.path.join(log_path,
                                 '%s_%s_log.log' %
                                 (get_local_time(), device))
    with open(log_file_name, 'w', encoding='utf-8') as f:
        f.flush()
    return log_file_name


@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射
    # 初始化 logger，设置日志级别为 info
    logger = logging.getLogger()
    logger.setLevel(level_relations.get('info'))

    global device
    log_file = makeLogDir(device, nameDir='log')
    # 获取当前运行文件名
    # file_name = get_current_file_name()
    # 定义日志格式和文件 handler
    formatter = logging.Formatter(
        f'%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d- %(levelname)s: %(message)s')
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 将文件handler添加到logger
    logger.addHandler(file_handler)

    yield

    # 在测试结束后移出文件 handler
    logger.removeHandler(file_handler)


# adb截图
def adb_screen_shot(fail_time=get_local_time()):
    '''
    adb截图
    :return:
    '''
    fail_pic = fail_time + ".png"
    pirtue_path = makeDir('pictures')
    pic_name = os.path.join(pirtue_path, fail_pic)
    cmd = 'adb shell /system/bin/screencap -p /sdcard/screenshot.png'
    subprocess.call(cmd, shell=True)
    cmd = 'adb pull /sdcard/screenshot.png {}'.format(pic_name)
    subprocess.call(cmd, shell=True)
    with open(pic_name, 'rb') as r:
        file_info = r.read()
    return file_info


# 报告优化
def pytest_html_report_title(report):
    report.title = "Automation Test Report Title!"


def pytest_configure(config):
    # 给环境表添加时间
    config._metadata['startTime'] = get_local_time()
    # 将环境表 移出 Packages和Plugins
    config._metadata.pop('Packages')
    config._metadata.pop('Plugins')


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    # 给环境表添加项目环境
    session.config._metadata['project environment'] = 'http:www.baid.com'


def pytest_html_results_summary(prefix, summary, postfix):
    #  追加的内容
    prefix.extend([html.p("Tester: qsgou")])


@pytest.fixture(scope='session', autouse=True)  # 自动执行
def browser():
    global driver
    if driver is None:
        driver = Base(device)
    yield driver


def pytest_html_results_table_header(cells):
    """
    处理结果表的表头
    """
    # 往表格增加一列Description，并且给Description列增加排序
    cells.insert(2, html.th("Description", class_="sortable desc", col="desc"))
    # 往表格增加一列Time，并且给Time列增加排序
    cells.insert(1, html.th("Time", class_="sortable time", col="time"))
    # 移除表格最后一列
    cells.pop()


def pytest_html_results_table_row(report, cells):
    """
    处理结果表的行
    """

    # 往列 Description插入每行的值
    cells.insert(2, html.th(report.description))
    # 往列 Time 插入每行的值
    cells.insert(1, html.th(datetime.utcnow(), class_="col-time"))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 定义列 Description的值，默认为测试方法的文档注释，如果测试方法没有文档注释，就自定义Description的值
    if str(item.function.__doc__) != "None":
        # 结果表的description列的值 = 测试方法的文档注释
        report.description = str(item.function.__doc__)
    else:
        # 结果表的description列的值 = 自定义的信息
        # 注意：这里可以将测试用例中的用例标题或者描述作为列 Description的值
        report.description = "The content described here"

    pytest_html = item.config.pluginmanager.getplugin("html")

    # 处理失败截图
    extra = getattr(report, "extra", [])
    resNmae = report.nodeid.split('/')[-1].replace("::", "-")  # 失败截图名称
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        # print(xfail is True, 333333)
        if (report.skipped and xfail) or (report.failed and not xfail):
            pirture_path = makeDir(dirName='./report/pictures')  # 判断图片存放目录，没有目录则创建;根目录为项目目录
            picture_name_path = fr'{pirture_path}{resNmae}.png'
            picture_name_path2 = fr'http://36.7.172.18:6026/static/qsgou_report/report/pictures/{resNmae}.png'
            # print('失败截图步骤')
            driver.getPicture(fileName=picture_name_path)
            # 增加HTML
            extra.append(pytest_html.extras.html(
                "<div style='background-color:red;text-align: center;font-size:16px;color:white;'> This case xfail or failed</div>"))
            extra.append(pytest_html.extras.image(picture_name_path2, name='failPicture'))
        report.extra = extra


if __name__ == '__main__':
    # adb_screen_shot()
    # print(get_local_time())
    # print(makeLogDir(device,nameDir='log'))
    # logging.info('testqsgou  1 == 1')
    # fail_pic = get_local_time() + ".png"
    # pirtue_path = makeDir('pictures')
    # pic_name = os.path.join(pirtue_path, fail_pic)
    # print(pic_name)
    print(project_root + "/log/failures")
