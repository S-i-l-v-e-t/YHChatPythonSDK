from bottle import route,request,run
import requests
import json
import threading
import time
onMsgList=[]
onTxtMsgList=[]
onCmdDict={}
btnEventDict={}
onFollowedList=[]
onUnfollowedList=[]
onJoinList=[]
onLeaveList=[]
reply={}
tok=''
class ThreadCtrl:
    threads=[]
    lock=threading.Lock()
    def __init__(self,func=lambda x="NoFunc":print(x),*args,init=False,**kwds):
        if init:
            ThreadCtrl.daemon=threading.Thread(target=ThreadCtrl.checker,daemon=True)
            ThreadCtrl.daemon.start()
        else:
            with ThreadCtrl.lock:
                ThreadCtrl.threads.append(self)
                self.func=func
                self.args=args
                self.kwds=kwds
                ThreadCtrl.threads[len(ThreadCtrl.threads)-1].initThread()
    def initThread(self):
        self.lock=threading.Lock()
        with self.lock:
            self._thread=threading.Thread(target=self.func,args=self.args,kwargs=self.kwds)
            self._thread.start()
    def getstat(self):
        with self.lock:
            self.rv= self._thread.is_alive()
        return self.rv
    @staticmethod
    def checker():
        while True:
            with ThreadCtrl.lock:
                for threadObj in ThreadCtrl.threads:
                    if not threadObj.getstat():
                        ThreadCtrl.threads.remove(threadObj)
            time.sleep(1)

def setToken(token):
    global tok
    tok=token
def editMsg(msgId,recvId,recvType,contentType,content='content',fileName='fileName',url='url',buttons=False):
    global headers,sjson,tok,reply
    headers = {'Content-Type': 'application/json'}
    sampleDict={
    "msgId": msgId,
    "recvId": recvId,
    "recvType": recvType,
    "contentType": contentType,
    "content": {
        "text": content
        }
    }
    if contentType=='image':
        sampleDict['content']={'imageUrl':url}
    if contentType=='file':
        sampleDict['content']={'fileName':fileName,'fileUrl':url}
    if buttons!=False:
        sampleDict['content']['buttons']=[buttons]
    sjson=json.dumps(sampleDict)
    #print(sjson)
    response=requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/edit?token={}".format(tok), headers=headers, data=sjson)
    reply=json.loads(response.text)
    print(reply)
def sendMsg(recvId,recvType,contentType,content='content',fileName='fileName',url='url',buttons=False):
    global headers,sjson,tok,reply
    headers = {'Content-Type': 'application/json'}
    sampleDict={
    "recvId": recvId,
    "recvType": recvType,
    "contentType": contentType,
    "content": {
        "text": content
        }
    }
    if contentType=='image':
        sampleDict['content']={'imageUrl':url}
    if contentType=='file':
        sampleDict['content']={'fileName':fileName,'fileUrl':url}
        
    if buttons!=False:
        sampleDict['content']['buttons']=[buttons]
    if type(recvId)==list:
        #sampleDict.update({'recvIds':sampleDict.pop("recvId")})
        #response=requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/batch_send?token={}".format(tok), headers=headers, data=sjson)
        #reply=json.loads(response.text)
        #print(reply)
        ##Alternative
        for yid in recvId:
            sampleDict['recvId']=yid
            sjson=json.dumps(sampleDict)
            response=requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={}".format(tok), headers=headers, data=sjson)
            reply=json.loads(response.text)
            print(reply)
            time.sleep(0.1)
    else:
        sjson=json.dumps(sampleDict)
        #print(sjson)
        response = requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={}".format(tok), headers=headers, data=sjson)
        reply=json.loads(response.text)
        print(reply)
# 批量发送消息
def batchSendMsg(recvIds, recvType, contentType, content):
    global sjson,tok,reply
    headers = {'Content-Type': 'application/json'}
    sampleDict= {
        "recvIds": recvIds,
        "recvType": recvType,
        "contentType": contentType,
        "content": {
            "text": content
        }
    }
    if contentType=='image':
        sampleDict['content']={'imageUrl':content}
    sjson=json.dumps(sampleDict)
    response = requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/batch_send?token={}".format(tok), headers=headers, data=sjson)
    reply=json.loads(response.text)
    print(reply)

def geneBaseBox(json,cnt=True):
    msgbox={}
    msgbox["type"]=json["event"]["chat"]["chatType"]
    if cnt:
        msgbox["contentType"]=json['event']['message']['contentType']
        if msgbox['contentType'] in ('text','markdown'):
            msgbox['msg']=json["event"]["message"]["content"]["text"]
        elif msgbox['contentType']=='image':
            msgbox['url']=json['event']['message']['content']['imageUrl']
        elif msgbox['contentType']=='file':
            msgbox['fileName']=json['event']['message']['content']['fileName']
            msgbox['url']=json['event']['message']['content']['fileUrl']
        elif msgbox['contentType']=='form':
            msgbox['form']=json['event']['message']['content']['formJson']
        msgbox['sender']=json["event"]["sender"]["senderId"]
        msgbox['senderInfo']={'nickname':json['event']['sender']['senderNickname'],'level':json['event']['sender']['senderUserLevel']}
    if msgbox['type']=='group' and cnt:
        msgbox["id"]=json["event"]["message"]["chatId"]
    elif msgbox['type']=='group' :
        msgbox['id']=json['event']['chatId']
        msgbox['nickname']=json['event']['nickname']
        msgbox['avatar']=json['event']['avatarUrl']
        msgbox['sender']=json["event"]["userId"]
    elif cnt:
        msgbox["id"]=json["event"]["sender"]["senderId"]
    else:
        msgbox['id']=json['event']['userId']
        msgbox['sender']=json['event']['userId']
        msgbox['nickname']=json['event']['nickname']
        msgbox['avatar']=json['event']['avatarUrl']
    if msgbox['type']=='group':
        msgbox['recvType']='group'
    elif msgbox['type']=='bot':
        msgbox['recvType']='user'
    return msgbox
@route("/sub",method='POST')
def onRecvPost():
    global sender
    json=request.json
    if json['header']['eventType']=="message.receive.normal":
        msgbox=geneBaseBox(json)
        for func in onMsgList:
            ThreadCtrl(func=func,ctx=msgbox)
        if msgbox['contentType'] in ("text","markdown"):
            for func in onTxtMsgList:
                ThreadCtrl(func=func,ctx=msgbox)
    elif json['header']['eventType']=='message.receive.instruction':
        cmd=json['event']['message']['commandName']
        if cmd in onCmdDict:
            msgbox=geneBaseBox(json)
            msgbox['cmd']=cmd
            ThreadCtrl(func=onCmdDict[cmd],ctx=msgbox)
    elif json['header']['eventType']=='bot.followed':
        msgbox=geneBaseBox(json,False)
        for func in onFollowedList:
            ThreadCtrl(func=func,ctx=msgbox)
    elif json['header']['eventType']=="bot.unfollowed":
        msgbox=geneBaseBox(json,False)
        for func in onUnfollowedList:
            ThreadCtrl(func=func,ctx=msgbox)
    elif json['header']['eventType']=="group.join":
        msgbox=geneBaseBox(json,False)
        for func in onJoinList:
            ThreadCtrl(func=func,ctx=msgbox)
    elif json['header']['eventType']=='group.leave':
        msgbox=geneBaseBox(json,False)
        for func in onLeaveList:
            ThreadCtrl(func=func,ctx=msgbox)
    elif json['header']['eventType']=='button.report.inline':
        msgbox={'type':json['event']['recvType'],'id':json['event']['recvId'],'value':json['event']['value']}
        if msgbox['value'] in btnEventDict:
            ThreadCtrl(func=btnEventDict[msgbox['value']],ctx=msgbox)
@route("/ping",method="GET")
def ping():
    return "pong"
class onLeave:
    def __init__(self,func):
        global onLeaveList
        self.func=func
        onLeaveList.append(func)
    def __call__(self, *args, **kwds):
        rv=self.func(*args,**kwds)
        return rv
class onJoin:
    def __init__(self,func):
        global onJoinList
        self.func=func
        onJoinList.append(func)
    def __call__(self, *args, **kwds):
        rv=self.func(*args,**kwds)
        return rv
class onUnfollowed:
    def __init__(self,func):
        global onUnfollowedList
        self.func=func
        onUnfollowedList.append(func)
    def __call__(self, *args, **kwds):
        rv=self.func(*args,**kwds)
        return rv
class onFollowed:
    def __init__(self,func):
        global onFollowedList
        self.func=func
        onFollowedList.append(func)
    def __call__(self, *args, **kwds):
        rv=self.func(*args,**kwds)
        return rv
class onTextMessage:
    def __init__(self,func):
        global onTxtMsgList
        self.func=func
        onTxtMsgList.append(func)
        print(onTxtMsgList)
    def __call__(self, *args, **kwds): 
        rv=self.func(*args,**kwds)
        return rv
class onMessage:
    def __init__(self,func):
        global onMsgList
        self.func=func
        onMsgList.append(func)
    def __call__(self, *args, **kwds): 
        rv=self.func(*args,**kwds)
        return rv
def onCommand(cmd):
    def deco(func):
        global onCmdDict
        if cmd not in onCmdDict:
            onCmdDict[cmd]=func
            #print(onCmdDict)
        def warpper(*args,**kwds):
            try:
                rv=func(*args,**kwds)
                return rv
            except:
                pass
        return warpper
    return deco
def onButtonPressed(cmd):
    def deco(func):
        global btnEventDict
        if cmd not in btnEventDict:
            btnEventDict[cmd]=func
            #print(onCmdDict)
        def warpper(*args,**kwds):
            try:
                rv=func(*args,**kwds)
                return rv
            except:
                pass
        return warpper
    return deco
def runBot(token='',port=7888):
    global tok
    tok=token
    ThreadCtrl(init=True)
    BottleThread=threading.Thread(run(host='0.0.0.0', port=port,loader=True))
    BottleThread.start()

