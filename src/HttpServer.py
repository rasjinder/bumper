"""
FILE:
   HttpServer.py

DESCRIPTION:
This class starts the Http server.

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

from http.server import BaseHTTPRequestHandler, HTTPServer # for 3.x.x 
#from  BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # for 2.x.x
from DbgLog import DbgLog
import threading

"""
CLASSNAME:
HttpServer

DESCRIPTION:
This class is responsible for starting a Http Server.
"""
class HttpServer(object):
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
        self.__thServer = ServerTh(self)
        self.__thServer.StartMe(self.__portNum)
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
    def __init__(self,webServer):
        threading.Thread.__init__(self)
#        self.__webServer = webServer
        self.__server = None
    
    """
    METHOD:
    StartMe (Public)
    
    DESCRIPTION:
    starts the server in thread
    
    RETURN VALUE:
    NONE
    """
    def StartMe(self,port): 
        DbgLog.TRACE(DbgLog.LVL_INFO,'Listening at port ' + str(port))
        self.__server = HTTPServer(('', port), ServerHndlr)
        self.start()  
    
    """
    METHOD:
    StopMe (Public)
    
    DESCRIPTION:
    stops the server
    
    RETURN VALUE:
    NONE
    """
    def StopMe(self):
        self.__server.server_close()
        
    """
    METHOD:
    run (Public)
    
    DESCRIPTION:
    Defining Thread body. Start listening on the port
    
    RETURN VALUE:
    NONE
    """
    def run(self):
        self.__server.serve_forever()

"""
CLASSNAME:
ServerHndlr

DESCRIPTION:
This is the handler for the HTTP server thread
"""            
class ServerHndlr(BaseHTTPRequestHandler):
    """
    METHOD:
    do_GET (Public)
    
    DESCRIPTION:
    Method to handle the HTTP-GET request
    
    RETURN VALUE:
    NONE
    """
    def do_GET(self):
        DbgLog.TRACE(DbgLog.LVL_INFO,'Got a request')
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
          
            #For 3.x.x
            self.wfile.write(bytes("<html><head><title>Title goes here.</title></head> ",'UTF-8'))
            self.wfile.write(bytes("<body><p>This is a test.</p>",'UTF-8'))
            self.wfile.write(bytes("</body></html>",'UTF-8'))
            # For 2.x.x  
            #self.wfile.write("<html><head><title>Title goes here.</title></head> ")
            #self.wfile.write("<body><p>This is a test.</p>")
            #self.wfile.write("</body></html>")
                
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     
    """
    METHOD:
    do_POST (Public)
    
    DESCRIPTION:
    Method to handle the HTTP-POST request
    
    RETURN VALUE:
    NONE
    """
#    def do_POST(self):
#        global rootnode
#        try:
#            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
#            if ctype == 'multipart/form-data':
#                query=cgi.parse_multipart(self.rfile, pdict)
#            self.send_response(301)
            
#            self.end_headers()
#            upfilecontent = query.get('upfile')
#            print "filecontent", upfilecontent[0]
#            self.wfile.write("<HTML>POST OK.<BR><BR>");
#            self.wfile.write(upfilecontent[0]);
            
#        except :
#            pass