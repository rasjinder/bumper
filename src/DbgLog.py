"""
FILE:
   DbgLog.py

DESCRIPTION:
This class Handles the creation of debug logs.

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
import datetime
import sys
import inspect

class DbgLog():
    LVL_INFO = 0
    LVL_WARN = 1
    LVL_ERR = 2
    """
    METHOD:
    TRACE
      
    DESCRIPTION:
    logging the data and displaying it on console
      
    RETURN VALUE:
    NONE
    """
    @classmethod
    def TRACE(cls,lvl,msg):
        lineNo = inspect.currentframe().f_back.f_lineno
        fileName = inspect.currentframe().f_back.f_code.co_filename
        pathstart = fileName.rfind("\\")
        if(pathstart == 0):
            pathstart = fileName.rfind("/")
        
        if(pathstart != 0):
            pathstart = pathstart + 1
            
        t = datetime.datetime.now().time()
        dbgMsg = str(t)[:-3] + ", " + fileName[pathstart:] + ":" + str(lineNo) + ", " 
        
        if lvl == DbgLog.LVL_ERR:
            dbgMsg = dbgMsg + "ERROR, " +  msg + "\n"
        elif lvl == DbgLog.LVL_WARN:
            dbgMsg = dbgMsg + "WARN, " +  msg + "\n"
        else:
            dbgMsg = dbgMsg + "INFO, " +  msg + "\n"
            
        FILE = open("gccmslog.csv","a")
        FILE.write(dbgMsg)
        FILE.close()
        sys.stdout.write(dbgMsg)