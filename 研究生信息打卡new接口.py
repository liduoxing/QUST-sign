# -*- coding: utf-8 -*-
# @Author  : cccht
# @Time    : 2022/9/2 14:14
# @Github  : https://github.com/cccht


# 安装模块命令
# pip install schedule
# pip install bs4
# pip install requests

# linux 后台运行命令
# nohup python3 -u 研究生信息打卡new接口.py >/home/log 2>&1 &

import json
import pathlib
import schedule
import os
import sys
import time
import requests
from bs4 import BeautifulSoup


class qust_gms():
    def __init__(self, stu_id, stu_password, server_key, szd, szd_text):
        self.stu_id = stu_id
        self.stu_password = stu_password
        self.server_key = server_key
        self.login_url = "https://gms.qust.edu.cn/login/enterLogin"
        self.signin_url = "https://gms.qust.edu.cn/login/signin"
        self.config_url = "https://gms.qust.edu.cn/sysCommon/getEzConfig"
        self.token = ""
        self.data_id_1 = ""
        self.data_id_2 = ""
        self.szd = szd
        self.szd_text = szd_text

    def login(self):
        mobile_login_url = "https://gms.qust.edu.cn/mobile/login"
        get_cookie_url = "https://gms.qust.edu.cn/mobile/getVerifyCodeBase64?uuid=&time=" + str(
            int(round(time.time() * 1000)))  # 获取毫秒级时间戳
        headers = {
            'referer': "https://gms.qust.edu.cn/",
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/105.0.0.0'
        }
        get_cookie = requests.get(get_cookie_url, headers=headers)
        self.token = get_cookie.headers['Set-Cookie'].split('=')[1].split(';')[0]
        uuid = json.loads(get_cookie.text)['uuid']
        false = False
        data_login = {
            'code': "",
            'password': self.stu_password,
            'rememberMe': false,
            'username': self.stu_id,
            'uuid': uuid
        }
        headers = {
            'cookie': 'JSESSIONID=' + self.token,
            'accept': "application/json, text/plain, */*",
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'origin': 'https://gms.qust.edu.cn',
            'referer': 'https://gms.qust.edu.cn/',
            'content-type': 'application/json;charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/105.0.0.0'
        }
        login_info = requests.post(mobile_login_url, data=json.dumps(data_login), headers=headers).text
        if (eval(login_info)['code']) == 200:
            print("\n# 已登录")
            self.get_form()
        else:
            print("\n# 账号或密码错误超过 5 次将被锁定，请登陆 https://gms.qust.edu.cn/login/enterLogin 确认密码！")
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
            "data": {"szd": self.szd, "tw": "37.2℃及以下", "stzk": "健康", "zgfxq": "否", "mj": "否", "ysbl": "否",
                     "yxgl": "否",
                     "jkmys": "绿色", "cn": "是", "szd_text": self.szd_text, "tw_text": "37.2℃及以下",
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


def index():
    try:
        print('\n# 打卡已启动')
        f = open('qust_gms.json', 'r', encoding='utf-8')
        content = f.read()
        info_list = json.loads(content)
        f.close()
        for info in info_list:
            if info['username'] == "" or info['password'] == "":
                print("请先填写完整 qust_gms.json 配置文件!按回车关闭。")
                input()
                return None
            username = info['username']
            password = info['password']
            server_key = info['server_key']
            szd = info['szd']
            szd_text = info['szd_text']
            print("\n# {} 账号信息已载入".format(username))
            qust_gms(username, password, server_key, szd, szd_text).login()
    except:
        # os.remove('qust_gms.json')  # 删除配置文件
        print("\n# 加载配置文件出错，请尝试修改，请重新运行此程序!按回车关闭。")
        input()
        sys.exit(0)


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
    std_list = []
    if not pathlib.Path("qust_gms.json").is_file():
        print(op_help())
        action_str = input()
        if action_str != '1':
            print('感谢您的使用！程序将于5s后退出。')
            time.sleep(5)
            sys.exit(0)
        os.system('cls')
        f = open('./qust_gms.json', 'a+', encoding="utf-8")
        while True:
            print("\n请输入学号：")
            username = input()
            print("\n请输入密码(使用 https://gms.qust.edu.cn/login/enterLogin 验证)：")
            password = input()
            print("\n请输入server酱密钥(用于推送打卡情况，可不填)：")
            server_key = input()
            szd = "370212"
            szd_text = "山东 - 青岛市 - 崂山区"
            print("\n是否修改打卡地址(默认为青岛市-崂山区，修改输入 1)：")
            check = input()
            if check:
                print("\n请输入区号(例如：青岛崂山为 370212)：")
                szd = input()
                print("\n请输入省份(例如：山东 具体可参照打卡系统名称)：")
                szd_text_1 = input()
                print("\n请输入市区(例如：青岛市 具体可参照打卡系统名称)：")
                szd_text_2 = input()
                print("\n请输入县(例如：崂山区 具体可参照打卡系统名称)：")
                szd_text_3 = input()
                szd_text = szd_text_1 + " - " + szd_text_2 + " - " + szd_text_3
            a = {
                "username": username,
                "password": password,
                "server_key": server_key,
                "szd": szd,
                "szd_text": szd_text
            }
            print(server_key)
            std_list.append(a)
            print("\n是否继续添加(需要请输入 1 并回车)：")
            continue_input = input()
            if continue_input != '1':
                break

        b = json.dumps(std_list, ensure_ascii=False)
        f.write(b)
        f.close()
    else:
        index()
        print('\n# 正在等待循环时间')
        schedule.every().day.at("07:00").do(index)
        while True:
            schedule.run_pending()
            time.sleep(59)


main()
