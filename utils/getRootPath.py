import configparser
import inspect
import os


def get_project_root():
    """Returns project root folder."""
    # 获取当前文件所在目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    # 获取项目根目录
    root_path = os.path.normpath(os.path.join(cur_path, ".."))
    return root_path.replace('\\', '/')


def get_current_file_name():
    """
    获取当前脚本文件名
    :return:
    """
    caller_file = inspect.getframeinfo(inspect.stack()[1][0]).filename
    # return os.path.splitext(os.path.basename(caller_file))[0]
    return os.path.abspath(caller_file).split('\\')[-1]


if __name__ == '__main__':
    # 获取当前文件名称、项目root路径、当前文件路径示例
    file_name = get_current_file_name()
    project_root = get_project_root()
    # file_path = project_root + '/utils/'+get_current_file_name()
    print(file_name)
    print(project_root)
    # print(file_path)
