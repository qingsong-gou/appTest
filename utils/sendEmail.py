import os
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from conftest import adb_screen_shot, get_local_time
from utils.getRootPath import get_project_root
from utils.operationConfig import OperationConfig
from utils.timeFormat import get_local_date

project_root = get_project_root()
oper = OperationConfig()

# login_url_report = oper.get_vlaue("serverAccount", 'login_url_report')  # 访问web地址，访问报告详情使用
url_report = oper.get_vlaue("serverAccount", 'url_report')  # 访问web地址，截图使用
name = oper.get_vlaue('emailAccount', 'name')  # 邮箱账户
authorization = oper.get_vlaue('emailAccount', 'authorization')  # 邮箱授权
receiver_to = eval(oper.get_vlaue('emailAccount', 'receiver_to'))  # 被发送人，读取默认为字符串，因此需要转list
receiver_cc = eval(oper.get_vlaue('emailAccount', 'receiver_cc'))  # 被抄送人


# print(url_report, name, authorization, receiver_to, receiver_cc)


class SMTP:
    def __init__(self, smtp_host="mail.iflymail.com.cn", port=465):
        # 连接邮件服务器
        self.__server = smtplib.SMTP_SSL(smtp_host, port)
        self.__sender = "词典笔自动化测试"  # 发件人邮箱账号
        self.__mailboxContainer = MIMEMultipart()  # 创建邮箱容器
        self.__receiver = []
        self.mail_from_name = "翻译笔自动化测试"

    def __del__(self):  # 对象销毁的时候,自动调用执行
        """
        关闭连接对象
        :return:
        """
        try:

            self.__server.quit()
        except Exception as e:
            pass

    def login(self, account, authorization):
        """登录邮箱服务器"""
        self.__sender = account
        self.__server.login(account, authorization)  # 括号中对应的是发件人邮箱账号、邮箱密码

    def add_subject(self, subject):
        """添加邮件主题"""
        self.__mailboxContainer['Subject'] = subject  # 邮箱主题

    def add_receiver(self, receiver_to: list, receiver_cc: list = None):
        """
        添加邮件接收人
        receiver_to：收件人
        receiver_cc：抄送人
        """
        self.__mailboxContainer["From"] = formataddr(pair=(self.mail_from_name, self.__sender))
        self.__mailboxContainer["To"] = ",".join(receiver_to)  # 邮箱接收人
        self.__mailboxContainer['Cc'] = ",".join(receiver_cc)  # 邮箱抄送人
        self.__receiver = receiver_to + receiver_cc

    def add_content(self, content, mail_type="plain", append_imgs: list = None):
        """
        添加邮箱内容
        content：邮箱内容
        mail_type：内容的类型
        append_imgs：当为html类型时追加图片内容
        """
        if mail_type != "html" and append_imgs is not None:
            raise ValueError(f"main_type的值不为html，但append_img不是空")

        if mail_type == "html" and append_imgs is not None:
            for append_img in append_imgs:
                img_tag = f"<p><img src='cid:image{append_imgs.index(append_img)}'></p>"
                content += img_tag
                # 读取图片信息
                with open(append_img, "rb") as f:
                    msg = f.read()
                msgImage = MIMEImage(msg, 'html')

                # 定义图片 ID，在 HTML 文本中引用
                msgImage.add_header('Content-ID', f'<image{append_imgs.index(append_img)}>')
                self.__mailboxContainer.attach(msgImage)
        self.__mailboxContainer.attach(MIMEText(content, mail_type, "utf-8"))

    def add_attach(self, file_path, filename):
        """添加单个附件"""
        if not os.path.exists(file_path):
            raise ValueError(f"文件【{file_path}】不存在")

        if not os.path.isfile(file_path):
            raise ValueError(f"【{file_path}】不是文件")

        # 构造文本附件
        with open(file_path, "rb") as f:
            msg = f.read()
        att = MIMEText(msg, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = f'attachment; filename="{filename}"'  # 这里的filename可以任意写，写什么名字，邮件附件中显示什么名字
        self.__mailboxContainer.attach(att)

    def add_attachs(self, file_paths: list):
        """添加多个附件"""
        for file_path in file_paths:
            self.add_attach(file_path)

    def send(self):
        """发送邮件"""
        self.__server.sendmail(self.__sender, self.__receiver, self.__mailboxContainer.as_string())

    def mail_content(self, appKey, builder, commitId, startTime, gitBranch, type="app_smoke"):
        '''

        :param appKey:
        :param builder:
        :param commitId:
        :param startTime:
        :param gitBranch:
        :return:
        '''
        if type == "app_regression":
            mail_content = f"""
            <h2>{appKey}应用自动化回归测试成功，请构建人{builder}关注</h2>
            <p>本次自动化冒烟测试执行概况如下：</p>
            <p>{builder}在{startTime}触发了一次{appKey}构建任务，构建commitid：{commitId}；构建分支：{gitBranch}</p>
            <p>报告内容如下，如需查看更多细节，请查看附件</p>
            <p>(此邮件是系统自动发出，不要回复此邮件)</p>
            """
        elif type == "app_performance":
            mail_content = f"""
            <h2>{appKey}应用自动化性能测试成功，请构建人{builder}关注</h2>
            <p>本次自动化冒烟测试执行概况如下：</p>
            <p>{builder}在{startTime}触发了一次{appKey}构建任务，构建commitid：{commitId}；构建分支：{gitBranch}</p>
            <p>报告内容如下，如需查看更多细节，请查看附件</p>
            <p>(此邮件是系统自动发出，不要回复此邮件)</p>
            """
        else:
            mail_content = f"""
            <h2>{appKey}应用自动化冒烟测试成功，请构建人{builder}关注</h2>
            <p>本次自动化冒烟测试执行概况如下：</p>
            <p>{builder}在{startTime}触发了一次{appKey}构建任务，构建commitid：{commitId}；构建分支：{gitBranch}</p>
            <p>报告内容如下，如需查看更多细节，请查看附件</p>
            <p>(此邮件是系统自动发出，不要回复此邮件)</p>
            """
        return mail_content


def get_phone_report_picture():
    '''
    手机访问报告地址并截图
    :return:
    '''
    os.system(
        f'adb shell am start -a android.intent.action.VIEW -d {url_report}')
    time.sleep(15)
    adb_screen_shot()


def get_web_report_picture():
    '''
    电脑访问报告地址并截图
    :return:
    '''
    options = webdriver.ChromeOptions()
    driver_path = project_root + "/driver/chromedriver.exe"
    driver = webdriver.Chrome(driver_path, options=options)
    # driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url_report)
    time.sleep(10)
    zoom_out = "document.body.style.zoom='0.6'"  # 屏幕比例缩小
    driver.execute_script(zoom_out)
    time.sleep(2)
    report_picture_name = project_root + rf"/pictures/{get_local_time()}_report.png"
    driver.save_screenshot(report_picture_name)
    time.sleep(3)
    driver.quit()
    return report_picture_name


def send_email(test_type='自动化'):
    '''
    发送文件
    待定项：获取当前软件版本
    :return:
    '''
    mailbox = SMTP()
    mailbox.login(name, authorization)

    # 添加邮箱主题
    mailbox.add_subject("使用SMTP封装类发送的邮件")

    mailbox.add_receiver(receiver_to, receiver_cc)

    # 添加邮箱内容
    send_time = get_local_date()
    mail_content = """
    <h2>%s版本%s冒烟测试失败，请构建人%s关注</h2>
    <p>本次自动化冒烟测试执行概况如下：</p>
    <p>%s在%s触发了一次rom构建任务，构建版本号：%s</p>
    <p>简陋报告内容如下，如需查看具体执行错误，请查看附件</p>
    <p>访问以下地址亦可查看详细报告：%s </p>
    <p>(此邮件是系统自动发出，不要回复此邮件)</p>
    """ % ("test", test_type, "qsgou", "qsgou", send_time, "test", url_report)
    report_picture_name = get_web_report_picture()
    append_imgs = [report_picture_name]
    # print(append_imgs)
    mailbox.add_content(mail_content, mail_type="html", append_imgs=append_imgs)

    # # 添加附件
    # mailbox.add_attach(project_root + fr"/report/{htmlName}", "test.html")
    #
    # 发送邮箱
    mailbox.send()


if __name__ == '__main__':
    # get_phone_report_picture()
    # print(get_web_report_picture())
    # driver_path = project_root + "/driver/chromedriver.exe"
    # print(driver_path)
    # mailbox = SMTP()
    # mailbox.login(account='cbg_cdb_autotest@iflymail.com.cn', authorization='aitest@2021')
    options = webdriver.ChromeOptions()
    driver_path = project_root + "/driver/chromedriver.exe"
    driver = webdriver.Chrome(driver_path, options=options)
    # driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url_report)
    time.sleep(10)
    zoom_out = "document.body.style.zoom='0.6'"
    driver.execute_script(zoom_out)
