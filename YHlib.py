from bottle import route,request,run
import requests
import json
import time
onMsgList=[]
reply={}
tok=''
def setToken(token):
    global tok
    tok=token
def sendMsg(recvId,recvType,contentType,content='content',fileName='fileName',url='url',buttons=False):
    global headers,sjson,tok
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
    #    sampleDict.update({'recvIds':sampleDict.pop("recvId")})
    #群发API疑似失效
        for yid in recvId:
            sampleDict['recvId']=yid
            sjson=json.dumps(sampleDict)
            response = requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={}".format(tok), headers=headers, data=sjson)
            reply=json.loads(response.text)
            print(reply)
            time.sleep(0.1)
    else:
        sjson=json.dumps(sampleDict)
        #print(sjson)
        response = requests.request("POST", "https://chat-go.jwzhd.com/open-apis/v1/bot/send?token={}".format(tok), headers=headers, data=sjson)
        reply=json.loads(response.text)
        print(reply)
msgbox={"id":0,"type":"bot",'msg':'String','sender':0}
@route("/sub",method='POST')
def onMessage():
    global sender
    json=request.json
    #print(json)
    msgbox["type"]=json["event"]["chat"]["chatType"]
    msgbox['msg']=json["event"]["message"]["content"]["text"]
    msgbox['sender']=json["event"]["sender"]["senderId"]
    if msgbox['type']=='group':
        msgbox["id"]=json["event"]["message"]["chatId"]
    else:
        msgbox["id"]=json["event"]["sender"]["senderId"]
    for func in onMsgList:
        func(ctx=msgbox)
@route("/ping",method="GET")
def ping():
    return "pong"
class onMessage:
    def __init__(self,func):
        global onMsgList
        self.func=func
        onMsgList.append(func)
    def __call__(self, *args, **kwds): 
        rc=self.func(*args,**kwds)
        return rc
def runBot(token,port=7888):
    global tok
    tok=token
    run(host='0.0.0.0', port=port,loader=True)

