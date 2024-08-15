import time

import pytest

from utils.getRootPath import get_project_root
from utils.sendEmail import send_email
from utils.uploadReport import uplod_zipfile


def excute():
    '''
    执行测试用例，并生成测试报告，上传服务器，发送测试邮件
    :return:
    '''
    project_root = get_project_root()
    pytest.main(
        ['-vs', f'--html={project_root}/report/report.html', f'--css={project_root}/config/report.css',
         '--self-contained-html',
         '--capture=sys'])  # 简陋报告
    print('----------report over----------')
    uplod_zipfile()  # 上传至服务器
    print('----------uplod over----------')
    send_email()  # 打开url_report截图并发送邮件
    print('----------over----------')


if __name__ == '__main__':
    project_root = get_project_root()
    pytest.main(
        ['-vs', f'--html={project_root}/report/report.html', f'--css={project_root}/config/report.css',
         '--self-contained-html',
         '--capture=sys'])  # 简陋报告
    print('----------report over------------')
    # t1 = time.time()
    # uplod_zipfile()  # 上传至服务器
    # print('----------uplod over------------')
    # send_email()  # 打开url_report截图并发送邮件
    # t2 = time.time()
    # print(t2 - t1)
    # print('----------over------------')
