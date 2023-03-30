import YHlib
_dbMaxLength=20
_db={}
def sendMsg(recvId,recvType,contentType,content='content',fileName='fileName',url='url',buttons=False):
    global _db,_dbMaxLength
    YHlib.sendMsg(recvId,recvType,contentType,content,fileName,url,buttons)
    if YHlib.reply['code']==1:
        _db[YHlib.reply['data']['messageInfo']['msgId']]={'recvId':recvId,'recvType':recvType,'contentType':contentType,'content':content,'fileName':fileName,'url':url,'buttons':buttons}
        if len(_db)>_dbMaxLength:
            _db.pop()
def editMsg(msgId,recvId,recvType,contentType,content='content',fileName='fileName',url='url',buttons=False):
    global _db,_dbMaxLength
    YHlib.editMsg(msgId,recvId,recvType,contentType,content,fileName,url,buttons)
    if YHlib.reply['code']==1:
        _db[msgId]={'recvId':recvId,'recvType':recvType,'contentType':contentType,'content':content,'fileName':fileName,'url':url,'buttons':buttons}
        if len(_db)>_dbMaxLength:
            _db.pop()
def getLastMsg():
    global _db
    return [_db[list(_db.keys())[0]],_db[list(_db.keys())[0]]]
def getMsgIdList():
    global _db
    klist=[]
    for k in _db.keys():
        if k not in klist:
            klist.append(k)
    return klist
def getMsgIdbyVar(**kwd):
    global _db
    var,content=list(kwd.items())[0]
    klist=[]
    for k in _db.keys():
        if (k not in klist) and _db[k][var]==content:
            klist.append(k)
    return klist
def getMsg(id=''):
    global _db
    return _db.get(id,None)
def setMaxLength(Length=20):
    global _dbMaxLength
    _dbMaxLength=Length
    return _dbMaxLength