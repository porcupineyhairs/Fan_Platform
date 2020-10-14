import os
import time

from faker import Faker

f = Faker(locale="zh_CN")


def get_cwd():
    path = os.path.split(os.path.dirname(__file__))[0]
    # 当前文件的绝对路径
    return path


def getPicPath():
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    project_path = get_cwd()
    Logs_path = os.path.join(project_path, 'Pics/')
    date_file_path = os.path.join(Logs_path, local_date + "/")
    # 如果没有日期文件夹，创建该文件夹
    if not os.path.exists(date_file_path):
        os.makedirs(date_file_path)
    picName = f.pystr()[:6] + ".PNG"
    return f"Pics/{local_date}/{picName}"


if __name__ == '__main__':
    path = os.path.split(os.path.dirname(__file__))[0]
    picPath = os.path.join(path, "Pics/2020-10-14/aQcbix.PNG")

    os.remove(picPath)
