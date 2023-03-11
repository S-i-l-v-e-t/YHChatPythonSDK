'''
Date: 2023-03-11 08:57:22
LastEditTime: 2023-03-11 09:14:36

Copyright (c) 2023 by S-i-l-v-e-t, All Rights Reserved. 
'''
import sys
sys.path.append('..')

from YHlib import setToken,sendMsg

class Message():
    def __init__(self):
        # 设置token
        # token字段值为机器人的Token，从云湖控制台获取
        setToken(token="xxx")


    ### 机器人给用户发送消息
    def send(self):
        # 第一个参数：机器人想发送给用户的用户ID
        # 第二个参数：对方为用户时，值为user
        sendMsg("7058262","user","text","HelloWorld")

if __name__ == "__main__":
    obj = Message()
    obj.send()