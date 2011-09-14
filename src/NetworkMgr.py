"""
FILE:
   NetworkMgr.py

DESCRIPTION:
This class Handles the network event which includes connection notifications.

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
from OSInterface import IpChangeNf
from OSInterface import GetAdapterInfo

"""
CLASSNAME:
NetworkMgr

DESCRIPTION:
This class handles the functionalities of the network manager. This
includes
    1. Tracking Connection Type
"""
class NetworkMgr(object):
    TUP_ADP_TYPE = 0
    TUP_ADP_IP = 1
    
    """
    METHOD:
    init
    
    DESCRIPTION:
    constructor
    
    RETURN VALUE:
    NONE
    """
    def __init__(self,clMgr):
        self.__clientMgr = clMgr
        self.__thIpChange = None
        self.__connType = Util.NW_STATE_UNKNOWN
        DbgLog.TRACE(DbgLog.LVL_INFO,"Connection Type: Unknown")
    
    def GetConnType(self):
        return self.__connType
    """
    METHOD:
    InitObj
    
    DESCRIPTION:
    starts the network manager
    
    RETURN VALUE:
    boolean - true if started successfully, false otherwise
    """
    def InitObj(self):   
        self.__UpdateConnType()
        self.__thIpChange = IpChangeNf(self.__clientMgr)
        self.__thIpChange.StartMe() 
        return True
        """
    METHOD:
    __UpdateConnType (Private)
    
    DESCRIPTION:
    Updates the connection type
    
    RETURN VALUE:
    NONE
    """ 
    def __UpdateConnType(self):
        tupAdapters = GetAdapterInfo()
        nConnType = -1
        if tupAdapters != None:
            nAdp = len(tupAdapters)
            if nAdp > 0:
                adp = tupAdapters[0]
                nConnType = adp[NetworkMgr.TUP_ADP_TYPE]
        if(self.__SetConnType(nConnType) == True):
            self.__clientMgr.PostEvent (Util.EVT_NW_STATE_CHANGE)
            DbgLog.TRACE(DbgLog.LVL_INFO,"Conn Change")
    """
    METHOD:
    __SetConnType (Private)
    
    DESCRIPTION:
    Sets the connection type
    
    RETURN VALUE:
    NONE
    """   
    def __SetConnType(self,nConnType):
        
        nOldConnType = self.__connType
        if nConnType == -1:
            self.__connType = Util.NW_STATE_DISCONN
            DbgLog.TRACE(DbgLog.LVL_INFO,"Connection Type: Disconnected")
        elif nConnType == 6:
            self.__connType = Util.NW_STATE_ETH
            DbgLog.TRACE(DbgLog.LVL_INFO,"Connection Type: Ethernet")
        elif nConnType == 71:
            self.__connType = Util.NW_STATE_WIFI
            DbgLog.TRACE(DbgLog.LVL_INFO,"Connection Type: Wifi")
        elif nConnType == 243 and nConnType == 244:
            self.__connType = Util.NW_STATE_WWAN
            DbgLog.TRACE(DbgLog.LVL_INFO,"Connection Type: 3G")
            
        if(nOldConnType == self.__connType):
            return False
        return True
    """
    METHOD:
    WrapUpObj
    
    DESCRIPTION:
    Wraps the object
    
    RETURN VALUE:
    NONE
    """  
    def WrapUpObj(self):
        self.__thIpChange = None
        if (self.__thIpChange != None):
            self.__thIpChange.StopMe()
            self.__thIpChange = None
    """
    METHOD:
    HandleEvt (Public)
    
    DESCRIPTION:
    Handles all the events which network manager needs to handle
    
    RETURN VALUE:
    NONE
    """  
    def HandleEvt(self,evt):
        if(evt == Util.EVT_IP_CHANGE):
            self.__UpdateConnType()
