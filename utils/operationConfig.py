from configparser import ConfigParser
import os
from utils.getRootPath import get_project_root

project_root = get_project_root()


class OperationConfig:
    def __init__(self, file_name="config.ini"):
        base_path = project_root + "/config"  # 配置文件所在目录
        self.file_path = os.path.join(base_path, file_name)
        self.config = ConfigParser()
        self.config.read(self.file_path)  # 打开文件

    def get_vlaue(self, section="test", option=None):
        """
        获取对应选项的值
        :param section: 节点名称
        :param option: 选项名称
        :return: 选项的值
        """
        if self.config.has_section(section=section):  # 如果section存在
            if self.config.has_option(section=section, option=option):  # 判断option是否存在
                return self.config.get(section=section, option=option)
            else:
                print(f"选项{option}不存在")
        else:
            print(f"节点{section}不存在")

    def set_value(self, section="test", option=None, value=None):
        """
        更新配置文件
        :param section: 节点名称
        :param option:  选项名称
        :param value:   选项的值
        :return:
        """
        with open(self.file_path, "r+") as fp:
            if self.config.has_section(section=section) is False:  # 如果节点不存在
                # 在配置文件中创建节点
                self.config.add_section(section=section)
            self.config.set(section=section, option=option, value=value)
            self.config.write(fp)


if __name__ == '__main__':
    oper = OperationConfig()

    name = oper.get_vlaue('emailAccount', 'name')  # 邮箱账户
    authorization = oper.get_vlaue('emailAccount', 'authorization')  # 邮箱授权
    receiver_to = eval(oper.get_vlaue('emailAccount', 'receiver_to'))  # 被发送人，读取默认为字符串，因此需要转list
    receiver_cc = eval(oper.get_vlaue('emailAccount', 'receiver_cc'))  #
    print(name,)
    print(authorization,)
    print(receiver_to,)
    print(receiver_cc,)
