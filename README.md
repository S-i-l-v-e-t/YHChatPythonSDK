# YHChatPythonSDK  

## UnOfficialSDK  

此 SDK 适用于 Python3.7 及以上版本。  
使用此 SDK 可以构建您的云湖机器人，能让您以非常便捷的方式和云湖服务进行交互。

目前实现的功能:消息发送，普通消息订阅接收，端口开放测试  
下一版本预计实现:所有类型订阅接收

## 依赖:
Bottle:
`pip install bottle`
requests:
`pip install requests`

## 使用方法：
要令一个函数进行消息接收，请引用本SDK并使用`@onMessage`装饰器
例子:
~~~
from YHLib import onMessage,runBot
@onMessage
def onRecvMsg(ctx):
    print(ctx)
runBot(token="xxx",port=7888)
~~~
要发送消息，请使用`sendMsg()`函数
### sendMsg参数:
recvId :String 接收者id,输入列表视为群发  
recvType :String 取值:"group";"user",接收者类型  
contentType :String 取值:"text";"image";"markdown";"file",消息类型  
content :String 消息正文，注意：这只在text和markdown类型下有效  
fileName :String 文件名，注意：这只在file类型下有效  
url :String 资源链接，注意：这只在file,image类型下有效  
buttons :List 按钮，具体内容请参阅[官方文档](https://www.yhchat.com/document/400-410),默认不适用  
#### 附注:按钮只需单层列表
例子:
~~~
from YHLib import setToken,sendMsg
setToken(token="xxx")
sendMsg("653505810","group","text","HelloWorld")
~~~

## 其他功能:
端口开放测试:
~~~
from YHLib import runBot,ping
runBot(token="xxx",port=7888)
~~~
之后使用浏览器访问  
`外网IP:7888/ping`  
成功看到pong即为端口开放成功
