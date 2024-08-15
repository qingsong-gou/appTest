import pymysql
from pymysql.cursors import DictCursor
from operationConfig import OperationConfig

# 获取数据库信息
oper = OperationConfig()
password = oper.get_vlaue("mysqlData", "password")
database = oper.get_vlaue("mysqlData", "database")
host = oper.get_vlaue("mysqlData", "host")
user = oper.get_vlaue("mysqlData", "user")
charset = oper.get_vlaue("mysqlData", "charset")
port = oper.get_vlaue("mysqlData", "port")


class Database(object):
    def __init__(self, password=password, database=database, host=host, user=user, charset=charset, port=int(port)):
        """
        创建连接对象
        :param password: 密码
        :param database: 要连接的数据库
        :param host: 主机的ip地址
        :param user: 用户
        :param charset: 编码
        :param port: 端口号
        """
        # 绑定初始化属性
        self.cnn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset=charset,
            database=database,
            port=port
        )

    def __del__(self):  # 对象销毁的时候,自动调用执行
        """
        关闭连接对象
        :return:
        """
        self.cnn.close()

    def fetchall(self, sql, args=None):
        """
        查询并获取所有的结果
        :param sql: 查询的sql语句
        :param args: 查询需要的参数
        :return: 查询结果
        """
        try:
            # 使用连接对象创建 字典类型的游标对象
            with self.cnn.cursor(DictCursor) as cursor:
                # 使用游标对象执行SQL语句
                cursor.execute(sql, args)
                # 使用游标对象获取所有执行结果
                data = cursor.fetchall()
            return data
        except Exception as e:
            print("代码错误:", e)
            return False

    def fetchone(self, sql, args=None):
        """
        查询并获取一条结果
        :param sql: 查询的sql语句
        :param args: 查询需要的参数
        :return: 查询结果

        """
        try:
            # 使用连接对象创建 字典类型的游标对象
            with self.cnn.cursor(DictCursor) as cursor:
                # 使用游标对象执行SQL语句
                cursor.execute(sql, args)
                # 使用游标对象获取一条执行结果
                data = cursor.fetchone()
            return data
        except Exception as e:
            print("代码错误:", e)
            return False

    def fetchmany(self, sql, args=None):
        """
        查询并获取多条结果
        :param sql: 查询的sql语句
        :param args: 查询需要的参数
        :return: 查询结果
        """
        try:
            # 使用连接对象创建 字典类型的游标对象
            with self.cnn.cursor(DictCursor) as cursor:
                # 使用游标对象执行SQL语句
                cursor.execute(sql, args)
                # 使用游标对象获取多条执行结果
                data = cursor.fetchmany()
            return data
        except Exception as e:
            print("查询出错:", e)
            return False

    def execute(self, sql, args=None):
        """
        使用一条增加,修改,删除 数据的语句
        :param sql: sql语句
        :param args: 参数
        :return: 成功:True , 失败:False
        """
        try:
            # 使用连接对象创建游标对象
            with self.cnn.cursor() as cursor:
                # 使用游标对象执行SQL语句
                num = cursor.execute(sql, args)
                if num == 1:  # 用受影响的行数,判断是否执行成功
                    self.cnn.commit()  # 成功就提交事务
                    return True
                else:
                    self.cnn.rollback()  # 不成功就进行回滚事务
                    return False
        except Exception as e:
            print("查询错误:", e)
            return False

    def executemany(self, sql, args):
        """
        使用多条增加,修改,删除 数据的语句
        :param sql: sql语句
        :param args: 参数
        :return: 成功:True , 失败:False
        """
        try:
            # 使用连接对象创建游标对象
            with self.cnn.cursor() as cursor:
                # 使用游标对象执行SQL语句
                num = cursor.execute(sql, args)
                if num == len(args):  # 判断受影响的行数是否和数据库中一致
                    self.cnn.commit()  # 成功就提交事务
                    return True
                else:
                    self.cnn.rollback()  # 不成功就进行回滚事务
                    return False
        except Exception as e:
            print("代码错误:", e)
            return False

    def create(self, sql, args=None):
        """
        用于执行受影响的行数为0的 所有sql语句
        :param sql: sql语句
        :param args: 参数
        :return: True   False
        """
        try:
            # 使用连接对象创建游标对象
            with self.cnn.cursor() as cursor:
                # 使用游标对象执行SQL语句
                cursor.execute(sql, args)
                return True
        except Exception as e:
            print("代码错误", e)
            return False


if __name__ == '__main__':  # 测试代码的书写位置
    db = Database()
    sql = "SELECT device_id from pm_device_info where device_sn=%s"
    device_sn = '1816A002052X004947W'
    data = db.fetchone(sql, device_sn)
    print(type(data))
    print(data)
