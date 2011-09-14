from CfgMgr import *
from DbgLog import DbgLog

class JsonParser():
    @classmethod
    def ParseReq(cls, reqData):#"{\"method\": \"%s\", \"params\": null, \"id\": null}"
        if(reqData[0] != "{" or reqData[-1] != "}"):
            DbgLog.TRACE(DbgLog.LVL_ERR,"Request not in proper format: " + reqData)
            return None
        kvPairs = reqData[1:-1].split(",")
        if(len(kvPairs) != 3):
            DbgLog.TRACE(DbgLog.LVL_ERR,"Request not in proper format: " + reqData)
            return None

        kvMth = kvPairs[0].split(":")
        kvParams = kvPairs[1].split(":")
        kvId = kvPairs[2].split(":")
        if(len(kvMth) != 2 or len(kvParams) != 2 or len(kvId) != 2):
            DbgLog.TRACE(DbgLog.LVL_ERR,"Request not in proper format: " + reqData)
            return None
        
        kvMthKey = kvMth[0].strip(' "')
        kvMthVal = kvMth[1].strip(' "')
        
        kvPrmsKey = kvParams[0].strip(' "')
        kvPrmsVal = kvParams[1].strip(' "')
        
        kvIdKey = kvId[0].strip(' "')
        kvIdVal = kvId[1].strip(' "')
        
        if(kvMthKey != "method" or kvPrmsKey != "params" or kvIdKey != "id"):
            DbgLog.TRACE(DbgLog.LVL_ERR,"Request not in proper format: " + reqData)
            return None
        rqObj = ReqObj(kvMthVal,kvPrmsVal,kvIdVal)
        return rqObj

    @classmethod
    def InQuotes(cls,msg):
        if(msg == None):
            return  None
        qstr = ("\"" + msg + "\"")
        return qstr

class ReqObj(object):
    def __init__(self,mth,prm,idVal):
        self.method = mth
        self.params = prm
        self.id = idVal
        
    def GetJsonStr(self):
        if(self.method == None):
            return None
        mthStr = JsonParser.InQuotes(self.method)
        prmStr = None
        idStr = None
        if(self.params == None):
            prmStr = "null"
        else:
            prmStr = self.params
            
        if (self.id == None):
            idStr = "null"
        else:
            idStr = JsonParser.InQuotes(self.id)
        
        jsonStr = CfgMgr.REQ_TXT %(mthStr,prmStr,idStr)
        return jsonStr
        
class RespObj(object):
    def __init__(self,res,err,idVal):
        self.result = res
        self.error = err
        self.id = idVal
        
    def GetJsonStr(self):#"{\"result\": %s, \"error\": %s, \"id\": %s}"
        if(self.result == None or self.error == None):
            return None
        resStr = self.result
        errStr = self.error
        idStr = None
            
        if (self.id == None):
            idStr = "null"
        else:
            idStr = JsonParser.InQuotes(self.id)
        
        jsonStr = CfgMgr.RESP_TXT %(resStr,errStr,idStr)
        return jsonStr
        