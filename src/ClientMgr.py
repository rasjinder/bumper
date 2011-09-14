"""
FILE:
   ClientMgr.py

DESCRIPTION:
This class starts the application and its message loop.

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
from Util import *
from CfgMgr import *
from StateMgr import StateMgr
#from HttpServer import HttpServer
from WebSockSrv import WebSockSrv
from NetworkMgr import NetworkMgr

"""
CLASSNAME:
ClientMgr

DESCRIPTION:
This class starts the application. This includes
    1. Starting the managers
    2. starting main event loop
""" 
class ClientMgr(object):   
    """
      METHOD:
      init (Public)
      
      DESCRIPTION:
      Constructor
      
      RETURN VALUE:
      NONE
    """          
    def __init__(self):
        DbgLog.TRACE(DbgLog.LVL_INFO,"Initializing ClientMgr")
        self.__evtQueue = [] # instance List variable
        self.__isEvtLoopOn = False
        self.__nwMgr = None
        self.__webMgr = None
        self.__stateMgr = None
        
    def GetNwMgr(self):
        return  self.__nwMgr
    """
    METHOD:
    initObj (Public)
      
    DESCRIPTION:
    initializing the client manager. Initializes all the managers
      
    RETURN VALUE:
    boolean - true if initialized successfully, false otherwise
    """
    def InitObj(self):
        if self.__InitStateMgr() == False:
            return False
        
        if self.__InitNwMgr() == False:
            return False
        
        if self.__InitWebMgr() == False:
            return False
        return True
  
    """
    METHOD:
    initNwMgr (Private)
    
    DESCRIPTION:
    initializing the Network manager
    
    RETURN VALUE:
    boolean - true if initialized successfully, false otherwise
    """
    def __InitStateMgr(self):
        self.__stateMgr = StateMgr()
        return True  
    """
    METHOD:
    initNwMgr (Private)
    
    DESCRIPTION:
    initializing the Network manager
    
    RETURN VALUE:
    boolean - true if initialized successfully, false otherwise
    """
    def __InitNwMgr(self):
        self.__nwMgr = NetworkMgr(self)
        if self.__nwMgr.InitObj() == False:
            DbgLog.TRACE(DbgLog.LVL_INFO,"Nw Manager init failed");
            return False
        return True
    
    """
    METHOD:
    initWebMgr (Private)
    
    DESCRIPTION:
    initializing the web socket server
    
    RETURN VALUE:
    boolean - true if initialized successfully, false otherwise
    """
    def __InitWebMgr(self):
        self.__webMgr = WebSockSrv(self,CfgMgr.PORT_NUM)
        if self.__webMgr.InitObj() == False:
            DbgLog.TRACE(DbgLog.LVL_INFO,"Web server init failed");
            return False
        return True
  
    """
    METHOD:
    WrapUpObj (Public)
    
    DESCRIPTION:
    Wraps all the managers object
    
    RETURN VALUE:
    NONE
    """
    def WrapUpObj(self):
        self.__isEvtLoopOn = False
         
        if self.__nwMgr != None:
            self.__nwMgr.WrapUpObj() 
            self.__nwMgr = None   
        
        if self.__webMgr != None:
            self.__webMgr.WrapUpObj() 
            self.__webMgr = None

    """
    METHOD:
    shutdown (Public)
        
    DESCRIPTION:
    stops the application
        
    RETURN VALUE:
    NONE
    """
    def Shutdown(self):
        self.WrapUpObj()
    
    """
    METHOD:
    postEvent (Public)
    
    DESCRIPTION:
    posts the event/message needs to be processed
    
    RETURN VALUE:
    NONE
    """
    def PostEvent(self, evt):
        #evtQLen = len(self.__evtQueue)
        self.__evtQueue.append(evt)
        DbgLog.TRACE(DbgLog.LVL_INFO,"Event added " + str(evt)) # + " at " + str(evtQLen))
        
    """
    METHOD:
    StartEventLoop (Public)
    
    DESCRIPTION:
    Starts the main event loop
    
    RETURN VALUE:
    NONE
    """   
    def startEventLoop(self):
        evtQLen = len(self.__evtQueue)
        if (evtQLen <= 0):
            return
        
        self.__isEvtLoopOn = True
        while (self.__isEvtLoopOn == True):#start an infinite loop
            evtQLen = len(self.__evtQueue)
            if (evtQLen > 0):
                self.__processEvent(self.__evtQueue[0])#process the event 
                self.__evtQueue[:1] = [] #removes the event
                DbgLog.TRACE(DbgLog.LVL_INFO,"Event processed-remaining " + str(evtQLen-1))
     
    """
    METHOD:
    processEvent (Private)
    
    DESCRIPTION:
    Process the event from the event queue
    
    RETURN VALUE:
    boolean - true if processed successfully, false otherwise
    """           
    def __processEvent(self, evt):
        DbgLog.TRACE(DbgLog.LVL_INFO,"Event processing "+ str(evt))
        if(evt == Util.EVT_INIT):
            if (self.InitObj() == False):
                self.shutdown()
        #elif (evt == Util.EVENT_IDLE ):
        #    self.__stateMgr.SetState(StateMgr.ST_RUNNING)
        elif (evt == Util.EVT_IP_CHANGE):
            if(self.__nwMgr != None):
                self.__nwMgr.HandleEvt(evt)
        elif (evt == Util.EVT_NW_STATE_CHANGE):
            if(self.__webMgr != None):
                self.__webMgr.HandleEvt(evt)
"""
METHOD:
main

DESCRIPTION:
Main function to start the application

RETURN VALUE:
NONE
""" 
def main():
    c = ClientMgr()
    c.PostEvent(Util.EVT_INIT)
    c.startEventLoop()

# main starting point for the application
if __name__ == '__main__':
    main()
        