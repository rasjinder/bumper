"""
FILE:
   OSInterface.py

DESCRIPTION:
This class implements all the OS related functionalities.

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

from ctypes import windll
import threading
from DbgLog import DbgLog
from Util import *

"""
CLASSNAME:
IpChangeTh

DESCRIPTION:
This class acts as a network thread and is responsible for capturing
the IP change notification from the OS
""" 
class IpChangeNf(threading.Thread):
    """
    METHOD:
    init
    
    DESCRIPTION:
    constructor
    
    RETURN VALUE:
    NONE
    """
    def __init__(self,clMgr):
        threading.Thread.__init__(self)
        self.__clientMgr = clMgr
        self.__isLoopOn = False
        self.__libtest = None
    
    """
    METHOD:
    StartMe
    
    DESCRIPTION:
    Starts the thread to register for the Ip notification loop
    
    RETURN VALUE:
    NONE
    """   
    def StartMe(self):
        self.__isLoopOn = True  
        self.start()  
        return True
    
    """
    METHOD:
    StopMe
    
    DESCRIPTION:
    Stops the thread for the Ip notification loop
    
    RETURN VALUE:
    NONE
    """ 
    def StopMe(self):
        self.__isLoopOn = False
    
    """
    METHOD:
    run
    
    DESCRIPTION:
    Defining Thread body. Start listening on the ip notification
    
    RETURN VALUE:
    NONE
    """
    def run(self):
        while self.__isLoopOn == True:
            DbgLog.TRACE(DbgLog.LVL_INFO,"Listening for Ip change")
            windll.iphlpapi.NotifyAddrChange(None,None)
            self.__clientMgr.PostEvent (Util.EVT_IP_CHANGE)
            
            DbgLog.TRACE(DbgLog.LVL_INFO,"Ip Change")
 
"""
METHOD:
GetAdapterInfo

DESCRIPTION:
Getting the adapter type and IP address in order

RETURN VALUE:
NONE
"""
def GetAdapterInfo():
    from ctypes import Structure, sizeof, pointer
    from ctypes import POINTER, byref, cast
    from ctypes import c_ulong, c_uint, c_ubyte, c_char
    
    MAX_ADAPTER_DESCRIPTION_LENGTH = 128
    MAX_ADAPTER_NAME_LENGTH = 256
    MAX_ADAPTER_ADDRESS_LENGTH = 8
    
    class IP_ADDR_STRING(Structure):
        pass
    LP_IP_ADDR_STRING = POINTER(IP_ADDR_STRING)
    IP_ADDR_STRING._fields_ = [
        ("next", LP_IP_ADDR_STRING),
        ("ipAddress", c_char * 16),
        ("ipMask", c_char * 16),
        ("context", c_ulong)]
    
    class IP_ADAPTER_INFO (Structure):
        pass
    LP_IP_ADAPTER_INFO = POINTER(IP_ADAPTER_INFO)
    IP_ADAPTER_INFO._fields_ = [
        ("next", LP_IP_ADAPTER_INFO),
        ("comboIndex", c_ulong),
        ("adapterName", c_char * (MAX_ADAPTER_NAME_LENGTH + 4)),
        ("description", c_char * (MAX_ADAPTER_DESCRIPTION_LENGTH + 4)),
        ("addressLength", c_uint),
        ("address", c_ubyte * MAX_ADAPTER_ADDRESS_LENGTH),
        ("index", c_ulong),
        ("type", c_uint),
        ("dhcpEnabled", c_uint),
        ("currentIpAddress", LP_IP_ADDR_STRING),
        ("ipAddressList", IP_ADDR_STRING),
        ("gatewayList", IP_ADDR_STRING),
        ("dhcpServer", IP_ADDR_STRING),
        ("haveWins", c_uint),
        ("primaryWinsServer", IP_ADDR_STRING),
        ("secondaryWinsServer", IP_ADDR_STRING),
        ("leaseObtained", c_ulong),
        ("leaseExpires", c_ulong)]
    
    GetAdaptersInfo = windll.iphlpapi.GetAdaptersInfo
    GetAdaptersInfo.restype = c_ulong
    GetAdaptersInfo.argtypes = [LP_IP_ADAPTER_INFO, POINTER(c_ulong)]
    
    adapterList = pointer(IP_ADAPTER_INFO())
    buflen = c_ulong(sizeof(adapterList))
    rc = GetAdaptersInfo(adapterList, byref(buflen))
    
    if(rc == 111): # Low memory
        newMem = (c_char * buflen.value)()
        adapterList = cast(newMem,POINTER(IP_ADAPTER_INFO))
        rc = GetAdaptersInfo(adapterList, byref(buflen))

    if rc !=0:
        return None
        
    a = adapterList.contents
    retAdpInfo = list()
    while a:
        adNode = a.ipAddressList
        while True:
            ipAddr = adNode.ipAddress
            if ipAddr and IsIpValid(ipAddr):
                adpInfo = (a.type,ipAddr)#tuple (type,IP)
                retAdpInfo.append(adpInfo)
            if adNode.next:
                adNode = adNode.next.contents
            else:
                break
        if a.next:
            a = a.next.contents
        else:
            break
    return (retAdpInfo)
"""
METHOD:
IsIpValid

DESCRIPTION:
Checking if the IP is valid

RETURN VALUE:
TRUE if the ip is valid False otherwise
"""
def IsIpValid(ip):
    if ip == None:
        return False
    
    ipStr = str(ip)
    if ipStr == "b'0.0.0.0'":
        return False
    return True