# CMDB
This is a auto collect hardware info CMDB system,build by Python Django.

##功能介绍
利用Django auth及permission模块实现功能权限管理
client程序把收集到的系统信息通过requests模块提交到服务端api
对采集到的资产信息进行初次审核，通过后如有变化自动更新。
Server端审核通过后可以指定设备位置显示在相应的机柜U位。

##开发环境
python3.5.2以上
Django 1.10.8
django-simple-serializer 2.0.7
djangorestframework 3.9.4

##服务端安装
服务器操作系统版本要求 centos7.4
git clone
通过Django makemigration创建数据库表结构
通过"python manage.py shell"修改admin密码
python manager.py runserver 0.0.0.0:<port>

##客户端收集汇报
python client.py
```
/config/settings.py
ASSET_API = 'http://<your_domain>/api_post/'
```

##访问
http://<your_server_ip>:<port>

##联系开发者
qq 2263917
