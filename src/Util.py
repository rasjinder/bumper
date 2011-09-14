"""
FILE:
   Util.py

DESCRIPTION:
This class defines all the common functionalities as well as constants
used for the application.

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

"""
CLASSNAME:
Util

DESCRIPTION:
This class defines all the common functionalities as well as constants
used for the application.
"""
class Util:
    # events used in the application
    EVT_INIT = 0
    EVT_STOP = 1
    EVT_IP_CHANGE = 2
    EVT_NW_STATE_CHANGE = 3
    EVT_NW_CONN_CHANGE = 4
    EVT_CFG_CHANGE = 5
    
    NW_STATE_UNKNOWN = -1
    NW_STATE_DISCONN = 0
    NW_STATE_ETH = 1
    NW_STATE_WIFI = 2
    NW_STATE_WWAN = 3
    

