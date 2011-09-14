"""
FILE:
   WebSockSrv.py

DESCRIPTION:
This class starts the Web socket server.

Copyright (C) 2010 QUALCOMM Incorporated. All rights reserved.
                   QUALCOMM Proprietary/GTDR

All data and information contained in or disclosed by this document is
confidential and proprietary information of QUALCOMM Incorporated and all
rights therein are expressly reserved.  By accepting this material the
recipient agrees that this material and the information contained therein
is held in confidence and in trust and will not be used, copied, reproduced
in whole or in part, nor its contents revealed in any manner to others
without the express written permission of QUALCOMM Incorporated.
"""

from DbgLog import DbgLog
from select import select
from Util import *
from CfgMgr import *
from JsonParser import JsonParser, ReqObj

import socket
import threading

"""
CLASSNAME:
WebSockSrv

DESCRIPTION:
This class is responsible for starting a web socket Server.
"""
class WebSockSrv(object):
    """
    METHOD:
    init (Public)
      
    DESCRIPTION:
    constructor
      
    RETURN VALUE:
    NONE
    """
    def __init__(self,clMgr,port):
        self.__clientMgr = clMgr
        self.__portNum = port
        self.__thServer = None

    """
    METHOD:
    InitObj (Public)
    
    DESCRIPTION:
    starts the server
    
    RETURN VALUE:
    boolean - true if started successfully, false otherwise
    """
    def InitObj(self):
        if self.__portNum <= 0:
            return False
    # in new thread
        self.__thServer = ServerTh(self, self.__portNum)
        self.__thServer.StartMe()
        return True; 

    """
    METHOD:
    WrapUpObj (Public)
    
    DESCRIPTION:
    Wraps the object
    
    RETURN VALUE:
    NONE
    """
    def WrapUpObj(self):
        self.__thServer.StopMe()
        self.__thServer = None
    
    """
    METHOD:
    HandleEvt (Public)
    
    DESCRIPTION:
    Handles all the events which Web socket server needs to handle
    
    RETURN VALUE:
    NONE
    """  
    def HandleEvt(self,evt):
        if self.__thServer == None:
            return
        if(evt == Util.EVT_NW_STATE_CHANGE):
            self.__thServer.SendNotification(evt)
    """
    METHOD:
    HandleReq (Public)
    
    DESCRIPTION:
    Handles all the request from the web socket client
    
    RETURN VALUE:
    NONE
    """     
    def HandleReq(self,reqObj):
        if self.__thServer == None:
            return
        
        if(reqObj.method == "network.state"):
            conn = self.__clientMgr.GetNwMgr().GetConnType()
            data = CfgMgr.RESP_TXT % (conn,"null",reqObj.id)
            self.__thServer.SendResp(data)
        elif(reqObj.method == "network.connectivity"):# TODO: sending Connectivity 
            data = CfgMgr.RESP_TXT % ("dummy","null",reqObj.id)
            self.__thServer.SendResp(data)
        elif(reqObj.method == "device.configuration"):# TODO: sending CFG info
            conn = self.__clientMgr.GetNwMgr().GetConnType()
            cfgTxt = CfgMgr.CFG_TXT%(JsonParser.InQuotes("1.0.0"),conn,JsonParser.InQuotes("dummy"))
            data = CfgMgr.RESP_TXT % (cfgTxt,"null",reqObj.id)
            self.__thServer.SendResp(data)
"""
CLASSNAME:
ServerTh

DESCRIPTION:
This is the server thread which listens HTTP requests on a port
"""      
class ServerTh(threading.Thread):
    """
    METHOD:
    init (Public)
      
    DESCRIPTION:
    constructor
      
    RETURN VALUE:
    NONE
    """
    def __init__(self, parent, port):
        threading.Thread.__init__(self)
        
        self.__parent = parent
        self.socket = None
        self.__port = port
        self.listeners = None 
        self.WebSocketObj = None
        self.__isThOn = False

    """
    METHOD:
    StartMe (Public)
    
    DESCRIPTION:
    starts the server in thread
    
    RETURN VALUE:
    NONE
    """
    def StartMe(self): 
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind(("localhost", self.__port))
        self.__listeners = [self.__socket] 
        self.start()  
    
    """
    METHOD:
    SendNotification (Public)
    
    DESCRIPTION:
    sends the notification to the websocket client
    
    RETURN VALUE:
    NONE
    """
    def SendNotification(self, ntf):
        if self.WebSocketObj == None:
            return
        if(ntf == Util.EVT_NW_STATE_CHANGE):
            req = ReqObj(CfgMgr.REQ_NW_STATE_TYPE,None,None)
            self.WebSocketObj.send(req.GetJsonStr())
        elif(ntf == Util.EVT_NW_CONN_CHANGE):
            req = ReqObj(CfgMgr.REQ_NW_CONN_TYPE,None,None)
            self.WebSocketObj.send(req.GetJsonStr())
        elif(ntf == Util.EVT_CFG_CHANGE):
            req = ReqObj(CfgMgr.REQ_CFG_TYPE,None,None)
            self.WebSocketObj.send(req.GetJsonStr())
    
    """
    METHOD:
    StartMe (Public)
    
    DESCRIPTION:
    starts the server in thread
    
    RETURN VALUE:
    NONE
    """
    def __ParseReq(self, data):
        if data[-1] != '\xff' or data[0] != '\x00':
            DbgLog.TRACE(DbgLog.LVL_ERR, "Request not in proper format: %s" % data)
            return
        reqData = data[1:-1]
        DbgLog.TRACE(DbgLog.LVL_INFO, "Got Req: %s" % reqData)
        reqObj = JsonParser.ParseReq(reqData)
        if(reqObj == None):
            return
        self.__parent.HandleReq(reqObj)
    """
    METHOD:
    SendResp (Public)
    
    DESCRIPTION:
    Sends the response to the websocket client
    
    RETURN VALUE:
    NONE
    """
    def SendResp(self, data):
        self.WebSocketObj.send(data)
    """
    METHOD:
    StopMe (Public)
    
    DESCRIPTION:
    stops the server
    
    RETURN VALUE:
    NONE
    """
    #def StopMe(self):
        #self.__server.server_close()
        
    """
    METHOD:
    run (Public)
    
    DESCRIPTION:
    Defining Thread body. Start listening on the port
    
    RETURN VALUE:
    NONE
    """
    def run(self):
        self.__socket.listen(10)
        DbgLog.TRACE(DbgLog.LVL_INFO,"Listening on %s" % self.__port)
        self.__isThOn = True
        while self.__isThOn:
            rList, wList, xList = select(self.__listeners, [], self.__listeners, 1)
            for ready in rList:
                if ready == self.__socket:
                    DbgLog.TRACE(DbgLog.LVL_INFO,"New client connection")
                    client, address = self.__socket.accept()
                    fileno = client.fileno()
                    self.__listeners.append(fileno)
                    self.WebSocketObj = WebSocket(client, self)
                else:
                    DbgLog.TRACE(DbgLog.LVL_INFO,"Client ready for reading %s" % ready)
                    client = self.WebSocketObj.client
                    dataBytes = client.recv(1024)
                    data = str(dataBytes,'utf-8')
                    fileno = client.fileno()
                    DbgLog.TRACE(DbgLog.LVL_INFO,"Got Message: %s" % data)
                    if data:
                        if(self.WebSocketObj.IsHandshakeDone() == False):
                            self.WebSocketObj.HndlHandshake(data)
                        else:
                            self.__ParseReq(data)
                    else:
                        DbgLog.TRACE(DbgLog.LVL_INFO,"Closing client %s" % ready)
                        self.WebSocketObj.close()
                        del self.WebSocketObj
            for failed in xList:
                if failed == self.__socket:
                    DbgLog.TRACE(DbgLog.LVL_INFO,"Socket broke")
                    self.WebSocketObj.close()
                    self.__isThOn = False
"""
CLASSNAME:
WebSocket

DESCRIPTION:
This class represents a web socket client.
"""
class WebSocket(object):
    HANDSHAKE = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n" + \
    "Upgrade: WebSocket\r\n" + \
    "Connection: Upgrade\r\n" + \
    "WebSocket-Origin: http://localhost:8888\r\n" + \
    "WebSocket-Location: ws://localhost:9999/\r\n\r\n" 
    
    """
    METHOD:
    init (Public)
      
    DESCRIPTION:
    constructor
      
    RETURN VALUE:
    NONE
    """
    def __init__(self, client, server):
        self.client = client
        self.__server = server
        self.__handshaken = False
        self.__header = ""
        self.__data = ""
    """
    METHOD:
    IsHandshakeDone (Public)
      
    DESCRIPTION:
    check if handshake done
      
    RETURN VALUE:
    True if done, False otherwise
    """
    def IsHandshakeDone(self):
        return self.__handshaken
    """
    METHOD:
    HndlHandshake (Public)
      
    DESCRIPTION:
    handle the handshake as send by web socket client
      
    RETURN VALUE:
    None
    """
    def HndlHandshake(self, data):
        if self.__handshaken == True:
            return
        self.__header += data
        if self.__header.find('\r\n\r\n') != -1:
            parts = self.__header.split('\r\n\r\n', 1)
            self.__header = parts[0]
            if self.__dohandshake(self.__header, parts[1]):
                DbgLog.TRACE(DbgLog.LVL_INFO,"Handshake successful")
                self.__handshaken = True
                
    """
    METHOD:
    __dohandshake (Public)
      
    DESCRIPTION:
    sends the handshake text as send by web socket client
      
    RETURN VALUE:
    True if send successfully, False otherwise
    """      
    def __dohandshake(self, header, key=None):
        DbgLog.TRACE(DbgLog.LVL_INFO,"Sending handshake %s" % WebSocket.HANDSHAKE)
        self.client.send(WebSocket.HANDSHAKE.encode())
        return True
                     
    #def onmessage(self, data):
    #    DbgLog.TRACE(DbgLog.LVL_INFO,"Got message: %s" % data)
    """
    METHOD:
    send (Public)
      
    DESCRIPTION:
    sends the data to web socket client
      
    RETURN VALUE:
    NONE
    """
    def send(self, data):
        if(data == None):
            return
        DbgLog.TRACE(DbgLog.LVL_INFO,"Sending message: %s" % data)
        dataStream = "\x00%s\xff" % data # creating a frame
        self.client.send(dataStream.encode())
    """
    METHOD:
    close (Public)
      
    DESCRIPTION:
    closes the web socket client
      
    RETURN VALUE:
    NONE
    """
    def close(self):
        self.client.close()
        