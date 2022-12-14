# 青科科技大学研究生打卡（请仔细阅读此文档）


请注意：**此脚本目前仅适用于青岛科技大学崂山校区信息学院研究生表单（每个表单的选项可能不一致）请自行查看之**

[青岛科技大学研究生管理系统 (qust.edu.cn)](https://gms.qust.edu.cn/login/enterLogin)

账号密码为以上网址的账户密码，在运行前请自行登录确认密码后再填入代码中

由于目前运行状态尚可，未考虑更多错误情况，之后如果有其他情况会再更新

## exe版本（即Windows可直接运行）
## 链接：https://github.com/cccht/QUST-sign/releases

## 最近更新

### 2022.9.2

原因：开发了手机端接口进行登录

更新内容：添加手机端接口文件，无需安装加密模块即可登录

### 2022.8.22 v1.2

原因：考虑到放假位置需要修改；上一版本耗费CPU资源较高；

更新内容：添加修改位置；修改睡眠时间降低CPU资源占用；修改打卡定时，默认为早7点，并且运行即打卡一次再进入等待；

温馨提示：Linux后台运行命令 `nohup python3 -u 研究生信息打卡.py >/home/log 2>&1 &`

### 2022.3.23 v1.1

原因：网站更新，系统一次即可打卡；系统添加防重复打卡机制，使用打卡与未打卡不同表单key

更新内容：删除try获取表单死循环，添加未打卡信息通信机制

### 2022.3.17 v1.0

上传cmd命令窗口版本及打包后exe文件，但测试阶段发现360会因exe窗口误杀，火绒则不会报毒。如果对exe文件存有怀疑请查看代码自行打包

# 禁止任何人使用此项目提供付费的代挂服务

## 不保证此脚本的运行结果，如果有错误请及时联系我

## **此项目默认提交全部正常的情况，如果有其他情况，请自行在系统上提交，项目目的仅为方便正常情况同学，严禁使用此项目伪造数据。疫情防疫严峻时刻请恪守学校要求**

#### 青岛科技大学研究生系统自动提交疫情上报py脚本，支持server酱推送提交结果消息

#### 使用了此脚本或者参考了这个项目，请自觉给项目点个star 如有需要也可随手点个 `Follow`

#### 本项目仅供学习交流使用，如作他用所承受的任何直接、间接法律责任一概与作者无关

#### 如果此项目侵犯了您或者您公司的权益，请立即联系我删除

#### 99%的问题都可以通过仔细阅读readme（使用说明，也叫项目说明）解决

#### 如有问题也可直接联系我


# 项目说明

- 打开项目中文件，填写账户密码，有需要可以填写server酱进行打卡情况推送


# 使用方式

1. **下载**

2. **安装模块（requests、Crypto等）**

   安装 `Crypto` 模块可参考[Python3.8 安装Crypto库 - cccht - 博客园 (cnblogs.com)](https://www.cnblogs.com/emmmmcccc/p/15990890.html)；使用new接口版本无需安装加密模块

3. **填写相关信息（学号、密码）**

4. **运行**

5. **完成表单填写**

# 说明

1. 再次声明 **此项目仅适用青岛科技大学崂山校区信息学院研究生表单**
2. 此项目依赖 `Python3.8` 如没有请自行安装
3. `Linux` 请安装相关环境
4. 此项目依赖 `requests Crypto json` 等Python库，如没有，请自行安装之
5. **此项目默认提交全部正常的情况，如果有其他情况，请自行在系统上提交，项目目的仅为方便正常情况同学，严禁使用此项目伪造数据。疫情防疫严峻时刻请恪守学校要求**

# 设计思路

1. 模拟登陆

2. 获取表单

3. 填充表单

4. 提交表单

5. 推送消息（通过server酱）

   **使用模拟的方式均为正常模拟，无攻击及其他违法行为，如有违反其他规定，请联系必删除之**

# 此外

我对于代码的规范上不是很懂，只是略微学过一点Python，如果有大能可以帮助完善只能是感激不尽

# 请作者喝杯奶茶？

如果你觉得对你有帮助也可以稍微微来杯奶茶~

![支付宝](https://github.com/cccht/QUST-sign/blob/main/zfb.jpg)
