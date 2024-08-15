"""
# @Time : 2023/8/9 11:27
# @Author : qsgou
# @FileName : uploadReport.py
# @ProjectName: 上传测试报告
"""
import os
import time
import zipfile

import paramiko
from conftest import project_root
from utils.operationConfig import OperationConfig

local_dir = f'{project_root}/report'
oper = OperationConfig()

report_path = oper.get_vlaue('serverAccount', 'report_path')  # 远程zip地址
remote_dir = oper.get_vlaue('serverAccount', 'remote_dir')  # 远程目录地址
hostname = oper.get_vlaue('serverAccount', 'hostname')  # 远程主机
username = oper.get_vlaue('serverAccount', 'username')  # 远程用户名
password = oper.get_vlaue('serverAccount', 'password')  # 远程用户密码


def zip_dir(root_dir):
    '''
    压缩文件夹
    '''
    zip_file_new = root_dir + ".zip"
    if os.path.exists(zip_file_new):
        os.remove(zip_file_new)
    zip = zipfile.ZipFile(zip_file_new, "w", zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(root_dir):
        fpath = dir_path.replace(root_dir, "")
        for file_name in file_names:
            zip.write(os.path.join(dir_path, file_name), os.path.join(fpath, file_name))
    zip.close()
    time.sleep(3)
    return zip_file_new


def uplod_zipfile():
    # 压缩文件
    local_zip_path = zip_dir(root_dir=local_dir)
    # 创建SSH客户端对象
    ssh_client = paramiko.SSHClient()
    # 设置自动添加主机密钥
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务器
    ssh_client.connect(hostname=hostname, username=username, password=password)
    sftp = ssh_client.open_sftp()
    sftp.put(local_zip_path, report_path)  # 上传报告
    try:
        ssh_client.exec_command(fr"rm -rf {remote_dir}")  # 删除上一次的报告
    finally:
        cmd = f"unzip -d {remote_dir}  {report_path}"
        ssh_client.exec_command(cmd)
        # 删除服务端报告压缩包
        ssh_client.exec_command(fr"rm -rf {report_path}")
        sftp.close()
        ssh_client.close()
        time.sleep(10)


if __name__ == "__main__":
    uplod_zipfile()
    # 上传新的报告
    # print("访问地址http://36.7.172.18:6026/static/qsgou_report/allure_report/index.html查看测试报告")
