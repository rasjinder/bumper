"""
FILE:
   StateMgr.py

DESCRIPTION:
This class stores the current state for the application.

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

"""
CLASSNAME:
StateMgr

DESCRIPTION:
This class stores the current state for the application.
"""

class StateMgr(object):
    ST_UNKNOWN = -1
    ST_INIT = 0
    ST_ERR = 1
    ST_RUNNING = 2
    ST_EXITING = 3
    """
    METHOD:
    init (Public)
      
    DESCRIPTION:
    constructor
      
    RETURN VALUE:
    NONE
    """
    def __init__(self):
        self.__state = StateMgr.ST_UNKNOWN
        DbgLog.TRACE(DbgLog.LVL_INFO," App state: Unknown ")
        
    def SetState(self,state):
        self.__state = state
        
    def GetState(self,state):
        return self.__state
            