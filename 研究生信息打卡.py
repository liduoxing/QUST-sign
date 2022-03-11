# -*- coding: utf-8 -*-
# @Author  : cccht
# @Time    : 2022/3/10 18:33
# @Github  : https://github.com/cccht

import base64
import json
# import schedule
import requests
from urllib import parse
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

stu_id = ''  # 此处填写学号
stu_password = ''  # 此处填写密码
server_key = ''  # 此处填写server酱密钥

login_url = "https://gms.qust.edu.cn/login/enterLogin"
signin_url = "https://gms.qust.edu.cn/login/signin"
config_url = "https://gms.qust.edu.cn/sysCommon/getEzConfig"


def index():
    print('打卡程序已运行...')
    try:
        headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        login = requests.get(login_url, headers=headers)
        token = login.headers['Set-Cookie'].split('=')[1].split(';')[0]
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

        rsa_password = encrypt(data_public_key, stu_password.encode()).decode('utf-8')
        headers = {
            'cookie': 'JSESSIONID=' + token,
            'origin': 'https://gms.qust.edu.cn',
            'referer': 'https://gms.qust.edu.cn/login/enterLogin',
            'x-requested-with': 'XMLHttpRequest',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        data_login = "loginForm=%7B%22loginId%22%3A%22" + stu_id + "%22%2C%22password%22%3A%22" + parse.quote(
            rsa_password) + "%22%2C%22verifyCode%22%3Anull%2C%22isWeekPassword%22%3Afalse%7D&token=" + token
        print(requests.post(signin_url, data=data_login, headers=headers).text)

        mrjkdk_url = "https://gms.qust.edu.cn/efm/collection/enterListTodoCollection?categoryId=mrjkdk"
        mrjkdk = requests.post(mrjkdk_url, data={'token': token}, headers=headers)
        soup = BeautifulSoup(mrjkdk.text, "html.parser")
        data_id_1 = soup.find(class_='card-btn').attrs['data-id']

        enterListRepeatedCollectionData_url = "https://gms.qust.edu.cn/efm/collection/enterListRepeatedCollectionData/" + data_id_1
        enterListRepeatedCollectionData = requests.post(enterListRepeatedCollectionData_url, data={'token': token},
                                                        headers=headers)
        soup = BeautifulSoup(enterListRepeatedCollectionData.text, "html.parser")
        data_id_2 = soup.find(class_='card-btn').attrs['data-id']

        enterViewCollectionData_url = "https://gms.qust.edu.cn/efm/collection/enterViewCollectionData/" + data_id_2
        requests.post(enterViewCollectionData_url, data={'token': token}, headers=headers)

        headers_submitCollectionData = {
            'cookie': 'JSESSIONID=' + token,
            'origin': 'https://gms.qust.edu.cn',
            'referer': 'https://gms.qust.edu.cn/login/enterMain/efm/collection/enterListMyCollection?categoryId=mrjkdk',
            'x-requested-with': 'XMLHttpRequest',
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62'
        }
        data = {
            "id": 'null',
            "collectId": data_id_1,
            "data": {"szd": "370212", "tw": "37.2℃及以下", "stzk": "健康", "zgfxq": "否", "mj": "否", "ysbl": "否", "yxgl": "否",
                     "jkmys": "绿色", "cn": "是", "szd_text": "山东 - 青岛市 - 崂山区", "tw_text": "37.2℃及以下", "stzk_text": "健康",
                     "zgfxq_text": "否", "mj_text": "否", "ysbl_text": "否", "yxgl_text": "否", "jkmys_text": "绿色",
                     "cn_text": "是"},
            "collectChildId": data_id_2
        }
        submitCollectionData_url = "https://gms.qust.edu.cn/efm/collection/submitCollectionData"
        submitCollectionData = requests.post(submitCollectionData_url, data=json.dumps(data),
                                             headers=headers_submitCollectionData)

        def send_message(data):
            print(data)            
            if server_key != '':
                header = {
                    'Content-type': 'application/x-www-form-urlencoded',
                }
                send_url = 'https://sctapi.ftqq.com/' + server_key + '.send'
                requests.post(send_url, data, headers=header)

        if json.loads(submitCollectionData.text)['code'] == 1:
            data = {
                'title': '研究生打卡成功！',
                'desp': '不要忘记放松心情哦~',
            }
            send_message(data)
        else:
            data = {
                'title': '研究生打卡失败！',
                'desp': '再次运行或者手动打卡吧~',
            }
            send_message(data)
    except:
        index()


index()
#schedule.every().day.at('10:00').do(index)
#while True:
#    schedule.run_pending()
