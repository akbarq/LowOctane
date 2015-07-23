#!/usr/bin/env python

from threading import *
import socket
import logging
import time
import sys
import signal
import os

print"""
####################################################################################################
# Description: LowOctane honeypot mimics Veeder-root Automatic Tank Gauge (ATG) systems.           #
#	       The honeypot listens on TCP port 10001 and only responds to fucntion code "I20100". #
#              All other function code requests from the client result in "9999FF1B" which means   #
#	       function code not recognized.							   #
# 	       This honeypot can be used to study attacks against ATG systems e.g. malicious use of #
#	       function codes against ATG systems. 						   #
# Version: 1.0											   #
# Author: Akbar Qureshi										   #
####################################################################################################
"""


if len(sys.argv) < 2:
    print 'Usage: lowoctance.py <ip_address>'
    print '\nExample: lowoctane.py 192.168.1.5' 
    print '\n'
    sys.exit(1)


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
port = 10001
host = sys.argv[1]

#updating timestamps on tank inventory status replies
date_time = time.strftime('%b %d, %Y %H:%M %p')

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.daemon = True
        self.start()

    def run(self):
        try:
            while 1:
		data = self.sock.recv(1024).decode('utf-8','ignore')
                logging.info('Client IP: %s | ATG Function Code: %s' %  (address[0],data))
		#Tank inventory report request function code "I20100" in hex.
	        if data == '\x01\x49\x32\x30\x31\x30\x30\x0d\x0a':
			#Sending tank inventory status to client 
               	    	self.sock.sendall(b"""

I20100
%s

Bobs Gas Station
2222 foobar drive
Miami, Fl
A7477740059476

IN-TANK INVENTORY

TANK PRODUCT               VOLUME TC-VOLUME   ULLAGE   HEIGHT    WATER    TEMP
  1  premium                 2348         0     4526    36.67     0.00   86.56
  2  Regular                 4231         0     5703    58.32     0.00   85.78
  3  Diesel                  5914         0     4870    33.58     0.00   88.73

""" % date_time)

                    
                else:
		     #All other fucntion code requests from the client returns "9999FF1B.". 
		     self.sock.sendall(b"9999FF1B\r\n")
        except socket.error as err:
            logging.info ("socket error  %s", err)
            return
        finally:
            self.sock.close()


#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
#port = 10001 #
#host = '0.0.0.0'


try:
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    logging.error ("Socket Error %s", err)
    exit(1)

try:
    serversocket.bind((host, port))
except socket.error as err:
    logging.error ("Cannot bind to address - %s", err)
    exit (1)


def sig_handler(signum, frame):
    raise OSError("control c caught: ")

signal.signal(signal.SIGINT, sig_handler)

serversocket.listen(5)
logging.info ("LowOctane listening on %s:%s" % (host,port))
while 1:
    try:
        clientsocket, address = serversocket.accept()
        client(clientsocket, address)
    except socket.error as err:
        logging.error ("Error - %s", err)
    except OSError: 
	logging.info ("Exiting all threads") 
        logging.shutdown()
        exit (0)

