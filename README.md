# YHChatPythonSDK  

## UnOfficialSDK  

此 SDK 适用于 Python3.7 及以上版本。  
使用此 SDK 可以构建您的云湖机器人，能让您以非常便捷的方式和云湖服务进行交互。

目前实现的功能:消息发送，所有类型(除按钮)订阅接收，端口开放测试  
TODO:  按钮订阅接收

## 依赖:
Bottle:  
`pip install bottle`  
requests:  
`pip install requests`  

## 使用方法：
**在一切开始之前，请*确保*你的订阅链接设置为`http://ip:port/sub`**  
要令一个函数进行消息接收，请引用本SDK并使用`@onMessage`装饰器  
要接收指令消息，请使用`@onCommand(cmd='commandName')`装饰器  
要接收关注消息，请使用`@onFollowed`装饰器  
要接收取关消息，请使用`@onUnfollowed`装饰器  
要接收入群消息，请使用`@onJoin`装饰器  
要接收退群消息，请使用`@onLeave`装饰器  
要只接受普通文本消息（包含text与markdown类型）请使用`@onTextMessage`装饰器  
例子:
~~~Python
from YHlib import onMessage,runBot
@onMessage
def onRecvMsg(ctx):
    print(ctx)
runBot(token="xxx",port=7888)
~~~  
### 要发送消息，请使用`sendMsg()`函数
#### sendMsg参数:
recvId :String 接收者id,输入列表视为群发  
recvType :String 取值:"group";"user",接收者类型  
contentType :String 取值:"text";"image";"markdown";"file",消息类型  
content :String 消息正文，注意：这只在text和markdown类型下有效  
fileName :String 文件名，注意：这只在file类型下有效  
url :String 资源链接，注意：这只在file,image类型下有效  
buttons :List 按钮，具体内容请参阅[官方文档](https://www.yhchat.com/document/400-410),默认不使用  
*附注:按钮只需单层列表*
例子:
~~~Python
from YHlib import setToken,sendMsg
setToken(token="xxx")
sendMsg("653505810","group","text","HelloWorld")
~~~
### 要编辑已发送消息，请使用`editMsg`函数  
#### editMsg参数:  
msgId :String 要编辑的消息id  
其余参数同sendMsg  
例子:  
~~~Python
from YHlib import setToken,editMsg
setToken(token="xxx")
editMsg(msgId='xxxxx',"653505810","group","text","HaveANiceDay")
~~~
### 要更快速的群发图片/文本消息,请使用`batchSendMsg()`函数
#### batchSendMsg参数  
recvIds :list 接收id列表  
recvType :String 取值:"group";"user",接收者类型  
contentType :String 取值:"text";"image";"markdown";"file",消息类型  
content :String 消息正文/图片Url  
### 多线程收发:  
要使用多线程执行，请确保你有充足的服务器资源，以YHlib-MultiThreading代替YHlib即可  
注意:使用多线程时请手动限制API调用频率
## 其他功能:
端口开放测试:
~~~Python
from YHlib import runBot,ping
runBot(token="xxx",port=7888)
~~~
之后使用浏览器访问  
`外网IP:7888/ping`  
成功看到pong即为端口开放成功  
  
## 小礼物:`Identify.py`,`msgDBmanager.py`:
针对目前没有官方的用户ID转用户名的api，制作了`Identify.py`这个基于关注和入群事件的转换脚本  
使用方法如下:  
~~~Python
import Identify
#Yid在此处代表用户id
print(Identify.fetch(Yid))
~~~  
针对目前没有官方的消息列表api，制作了`msgDBmanager.py`这个基于字典的消息列表管理模块  
使用方法如下:  
~~~Python
from YHlib import setToken
from msgDBmanager import *
setToken(token='xxx')
setMaxLength(20)
#设置存储消息最大数量，默认不设置为20条
sendMsg("653505810","group","text","HelloWorld")
editMsg(getLastMsg()[0],**getLastMsg()[1])
#getLastMsg() -> List:
#[0]:msgId
#[1]:arguments -> Dict:详见下方getMsg输出
print(getMsgIdList())
#Output: ['id1','id2',...]
#注:此模块仅记录通过模块发送的消息,如上述例子，id1应等同于getLastMsg[0]
print(getMsgIdByVar(content='HelloWorld'))
#Output: ['id1',]
#注:参数即为需搜索项,content即搜索内容,recvId即搜索接收方
print(getMsg('id1'))
#Output: {'recvId':'653505810','recvType':'group','contentType':'text','content':'HelloWorld','fileName':"fileName",'url':"url",'buttons':False}
~~~  
