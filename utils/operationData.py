"""
文件名:operation_data.py
作用:读取Excel表格和CSV文件,将excel数据读取成[{},{}]格式
"""
import json
import os

import numpy
import pandas
import yaml
from jsonpath import jsonpath

from utils.getRootPath import get_project_root

project_root = get_project_root()


class OperationExcelData:
    def __init__(self, filename, sheet_name=0):
        """
        通过传入的文件名,可以判其是yaml格式还是Excel格式,根据不同格式
        作出相应处理
        """
        # 得到存放数据的目录--数据在data文件夹中
        self.file_path = project_root + "/data/" + filename

        # 通过文件名判断文件格式
        file_type = filename.split(".")[-1]
        if file_type in ['xlsx', 'xls']:
            self.file = pandas.read_excel(self.file_path, keep_default_na=False,
                                          sheet_name=sheet_name)  # 如果是Excel,通过read_Excel读取

    def get_data_to_dict(self):
        """将文件数据获取成[{},{}]格式"""
        return [self.file.loc[i].to_dict() for i in self.file.index.values]

    def get_data_to_list(self):
        """将文件数据获取成[[],[]]格式"""
        return self.file.values.tolist()


class NpEncoder(json.JSONEncoder):
    """pandas int64类型转换"""

    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def get_key_value(json_data, keyword=None):
    '''
    根据字段获取值,返回list
    :return:
    '''
    data_list = jsonpath(json_data, f"$..{keyword}")
    return data_list


def get_yaml(yaml_name):
    result = None
    yamlPath = project_root + '/data/' + yaml_name
    try:
        with open(yamlPath, 'r', encoding='utf-8') as f:
            data = f.read()
        result = yaml.load(data, Loader=yaml.FullLoader)  # FullLoafer可以yaml解析变得安全
        return result
    except Exception as e:
        print(e, '获取yaml数据异常')
    finally:
        return result


def makeDir(dirName):
    '''
    检查并创建文件夹
    :return:
    '''
    log_path = os.path.join(project_root,
                            dirName)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path + '\\'


if __name__ == '__main__':
    # yaml_data = get_yaml(yaml_name='test.yaml')
    # receiver_to = get_key_value(yaml_data, keyword='pad_pwd')
    # receiver_cc = get_key_value(yaml_data, keyword='memberId')
    # print(receiver_cc, receiver_to)
    # oper = OperationExcelData(filename="wifi_data.xlsx", sheet_name=0)
    # wifi_data_success = oper.get_data_to_list()
    # oper2 = OperationExcelData(filename="wifi_data.xlsx", sheet_name=1)
    # wifi_data_fail = oper2.get_data_to_list()
    # print(wifi_data_fail, '失败')
    # print(wifi_data_success, '成功')
    print(makeDir('./report/1111'))
