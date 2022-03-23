# -*- coding: utf-8 -*-
# @Author  : cccht
# @Time    : 2022/3/23 10:08
# @Github  : https://github.com/cccht


import base64
import json
import pathlib

import schedule
import os
import sys
import time

import requests
from urllib import parse
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5


class qust_gms():
    def __init__(self, stu_id, stu_password, server_key, schedule_check, schedule_time):
        self.stu_id = stu_id
        self.stu_password = stu_password
        self.server_key = server_key
        self.login_url = "https://gms.qust.edu.cn/login/enterLogin"
        self.signin_url = "https://gms.qust.edu.cn/login/signin"
        self.config_url = "https://gms.qust.edu.cn/sysCommon/getEzConfig"
        self.token = ""
        self.data_id_1 = ""
        self.data_id_2 = ""
        self.schedule_check = schedule_check
        self.schedule_time = schedule_time

    def login(self):
        headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        login = requests.get(self.login_url, headers=headers)
        self.token = login.headers['Set-Cookie'].split('=')[1].split(';')[0]
        soup = BeautifulSoup(login.text, "html.parser")
        data_public_key = soup.find(id='password').attrs['data-public-key']
        pub = '\n'.join([
            '-----BEGIN PUBLIC KEY-----\n' + data_public_key + '\n-----END PUBLIC KEY-----'
        ])
        data_public_key = RSA.importKey(pub)

        def encrypt(public_key, message):
            cipher = Cipher_pkcs1_v1_5.new(public_key)
            cipher_text = base64.b64encode(cipher.encrypt(message))
            return cipher_text

        rsa_password = encrypt(data_public_key, self.stu_password.encode()).decode('utf-8')
        headers = {
            'cookie': 'JSESSIONID=' + self.token,
            'origin': 'https://gms.qust.edu.cn',
            'referer': 'https://gms.qust.edu.cn/login/enterLogin',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        data_login = "loginForm=%7B%22loginId%22%3A%22" + self.stu_id + "%22%2C%22password%22%3A%22" + parse.quote(
            rsa_password) + "%22%2C%22verifyCode%22%3Anull%2C%22isWeekPassword%22%3Afalse%7D&token=" + self.token
        login_info = requests.post(self.signin_url, data=data_login, headers=headers).text
        null = None
        true = True
        false = False
        if (eval(login_info)['code']) == 1:
            print("\n# 已登录")
            self.get_form()
        else:
            print("\n账号或密码错误，请登陆 https://gms.qust.edu.cn/login/enterLogin 确认密码！")
            input()
            sys.exit(0)

    def get_form(self):
        headers = {
            'cookie': 'JSESSIONID=' + self.token,
            'origin': 'https://gms.qust.edu.cn',
            'referer': 'https://gms.qust.edu.cn/login/enterLogin',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        mrjkdk_url = "https://gms.qust.edu.cn/efm/collection/enterListTodoCollection?categoryId=mrjkdk"
        mrjkdk = requests.post(mrjkdk_url, data={'token': self.token}, headers=headers)
        soup = BeautifulSoup(mrjkdk.text, "html.parser")
        self.data_id_1 = soup.find(class_='card-btn').attrs['data-id']
        enterListRepeatedCollectionData_url = "https://gms.qust.edu.cn/efm/collection/enterListRepeatedCollectionData/" + self.data_id_1
        enterListRepeatedCollectionData = requests.post(enterListRepeatedCollectionData_url,
                                                        data={'token': self.token},
                                                        headers=headers)
        soup = BeautifulSoup(enterListRepeatedCollectionData.text, "html.parser")
        self.data_id_2 = soup.find(class_='card-btn').attrs['data-id']
        enterViewCollectionData_url = "https://gms.qust.edu.cn/efm/collection/enterViewCollectionData/" + self.data_id_2
        requests.post(enterViewCollectionData_url, data={'token': self.token}, headers=headers)

        print("\n# 已获取表单数据")
        self.submit_form()  # 调用提交


    def submit_form(self):
        print("\n# 正在提交")
        headers_submitCollectionData = {
            'cookie': 'JSESSIONID=' + self.token,
            'origin': 'https://gms.qust.edu.cn',
            'referer': 'https://gms.qust.edu.cn/login/enterMain/efm/collection/enterListMyCollection?categoryId=mrjkdk',
            'x-requested-with': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        data = {
            "id": 'null',
            "collectId": self.data_id_1,
            "data": {"szd": "370212", "tw": "37.2℃及以下", "stzk": "健康", "zgfxq": "否", "mj": "否", "ysbl": "否",
                     "yxgl": "否",
                     "jkmys": "绿色", "cn": "是", "szd_text": "山东 - 青岛市 - 崂山区", "tw_text": "37.2℃及以下",
                     "stzk_text": "健康",
                     "zgfxq_text": "否", "mj_text": "否", "ysbl_text": "否", "yxgl_text": "否", "jkmys_text": "绿色",
                     "cn_text": "是"},
            "collectChildId": self.data_id_2
        }
        submitCollectionData_url = "https://gms.qust.edu.cn/efm/collection/submitCollectionData"
        submitCollectionData = requests.post(submitCollectionData_url, data=json.dumps(data),
                                             headers=headers_submitCollectionData)

        def send_message(data, server_key):
            print("\n" + data['desp'])
            if server_key == "":
                return None
            header = {
                'Content-type': 'application/x-www-form-urlencoded',
            }
            send_url = 'https://sctapi.ftqq.com/' + server_key + '.send'
            requests.post(send_url, data, headers=header)

        # print(submitCollectionData.text)
        try:
            if json.loads(submitCollectionData.text)['code'] == 1:
                data = {
                    'title': '研究生打卡成功！',
                    'desp': '# 打卡成功！阴霾终将散去，让我们携手共克时艰！加油！！！',
                }
                send_message(data, self.server_key)
            else:
                data = {
                    'title': '研究生打卡失败！',
                    'desp': '# 打卡失败，再次运行或者手动打卡吧~~~',
                }
                send_message(data, self.server_key)
        except:
            print("或许您已提交打卡，请您前往网站查看。")
            data = {
                'title': '研究生打卡失败！',
                'desp': submitCollectionData.text,
            }
            send_message(data, self.server_key)
            return None

    def index(self):
        print('\n# 打卡已启动')
        if self.schedule_check:
            print('\n# 正在等待循环时间')
            schedule.every().day.at(self.schedule_time).do(self.login)
            while True:
                schedule.run_pending()
        else:
            self.login()


def op_help():
    return """
#### 首次使用，请您花费两分钟时间阅读以下信息 ####

说明:
    1. 此一键打卡仅针对一切正常的同学，如有其他情况请登录网站自行打卡！！！

    2. 账户密码需要登录 https://gms.qust.edu.cn/login/enterLogin 测试 

    3. 此一键打卡免费开源，免费使用即可，项目地址为 https://github.com/cccht/QUST-sign

    4. 制作此程序初衷为方便同学、及时提交打卡信息，且方式正常，无攻击及其他恶意行为，如违反相关规定GitHub联系必删除

    5. 本人编程水平有限，如有更高效的方式想共同交流改进，也请通过GitHub联系

再次注意！此程序仅针对身体状况正常的同学，如果有其他情况请 一定 不要使用此程序！

如果您同意且身体状况正常，请输入 1 确认使用此程序："""


def main():
    # 此处处理配置文件，如果无则创建，如果有则读取相关信息
    global username, password, server_key, schedule_check, schedule_time
    # if not os.path.exists('qust_gms.json'):
    if not pathlib.Path("qust_gms.json").is_file():
        print(op_help())
        action_str = input()
        if action_str != '1':
            print('感谢您的使用！程序将于5s后退出。')
            time.sleep(5)
            sys.exit(0)
        os.system('cls')
        print("请输入学号：")
        username = input()
        print("\n请输入密码(使用 https://gms.qust.edu.cn/login/enterLogin 验证)：")
        password = input()
        print("\n请输入server酱密钥(用于推送打卡情况，可不填)：")
        server_key = input()
        schedule_check = False
        hour = '07'
        minute = '00'
        print("\n是否需要定时功能(需要请输入 1 并回车)：")
        check = input()
        if check:
            schedule_check = True
            print("\n请输入几时(注意：7 点输入 07，下午 1 点输入 13)：")
            hour = input()
            print("\n请输入几分(注意：7 分输入 07，整点输入 00)：")
            minute = input()
        schedule_time = hour + ':' + minute
        a = {
            "username": username,
            "password": password,
            "server_key": server_key,
            "schedule_check": schedule_check,
            "schedule_time": schedule_time
        }
        print(server_key)
        b = json.dumps(a, ensure_ascii=False)
        f = open('./qust_gms.json', 'w', encoding="utf-8")
        f.write(b)
        f.close()
    else:
        try:
            f = open('qust_gms.json', 'r', encoding='utf-8')
            content = f.read()
            qust = json.loads(content)
            f.close()
            if qust['username'] == "" or qust['password'] == "":
                print("请先填写完整 qust_gms.json 配置文件!按回车关闭。")
                input()
                return None
            username = qust['username']
            password = qust['password']
            server_key = qust['server_key']
            schedule_check = qust['schedule_check']
            schedule_time = qust['schedule_time']
        except:
            os.remove('qust_gms.json')
            print("加载配置文件出错，请重新运行此程序!按回车关闭。")
            input()
            sys.exit(0)
    os.system('cls')
    print("# 账号信息已载入")
    qust_gms(username, password, server_key, schedule_check, schedule_time).index()
    input()
    sys.exit(0)


main()
