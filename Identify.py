from YHlib import *
idbase={}
def fetch(Yid):
    global idbase
    return idbase.get(Yid,Yid)
def _wdb():
    global idbase
    with open("./database/idbase.sdb",'w',encoding='utf-8') as f:
        f.write(str(idbase))
@onJoin
def join(ctx):
    global idbase
    idbase[ctx['sender']]=ctx['nickname']
    _wdb()
@onFollowed
def fld(ctx):
    global idbase
    idbase[ctx['sender']]=ctx['nickname']
    _wdb()
with open("./database/idbase.sdb",encoding='utf-8') as f:
    idbase=eval(f.read())