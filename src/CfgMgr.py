class CfgMgr:
    PORT_NUM = 8080
    
    REQ_TXT = "{\"method\": %s, \"params\": %s, \"id\": %s}"
    REQ_NW_STATE_TYPE = "network.state"
    REQ_NW_CONN_TYPE = "network.connectivity"
    REQ_CFG_TYPE = "network.configuration"
    
    RESP_TXT = "{\"result\": %s, \"error\": %s, \"id\": %s}"
    RESP_STATE_TYPE = "network.state"
    RESP_CONN_TYPE = "network.connectivity"
    RESP_CFG_TYPE = "network.configuration"

    CFG_TXT = "{\"version\":%s, \"network.state:\":%s, \"network.connectivity\":%s}"