#!/usr/bin/env python
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import pynotify
import mpd
import time
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  

Icon="file:///home/xcorp/src/mpd-pynotify/sonata.png"

## Some functions
def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

def mpdAuth(client, secret):
    """
    Authenticate
    """
    try:
        client.password(secret)
    except CommandError:
        return False
    return True
##

def main():
    
    ##Notify init
    if not pynotify.init("mpd-pynotify"):
        sys.exit(1)
    notify = pynotify.Notification("MPD Notification")
    notify.set_urgency(pynotify.URGENCY_CRITICAL)
    
    
    ## MPD object instance
    client = mpd.MPDClient()
    if mpdConnect(client, CON_ID):
        pass
    else:
        print 'fail to connect MPD server.'
        sys.exit(1)

    # Auth if password is set non False
    if PASSWORD:
        if mpdAuth(client, PASSWORD):
            print 'Pass auth!'
        else:
            print 'Error trying to pass auth.'
            client.disconnect()
            sys.exit(2)
    
    prevsong=client.playlistinfo()[int(client.status()["song"])]
    while True:
        client.idle()
        currsong=client.playlistinfo()[int(client.status()["song"])]
        if not prevsong == currsong:
            prevsong = currsong
            notify.update(client.playlistinfo()[int(client.status()["song"])]["title"],client.playlistinfo()[int(client.status()["song"])]["artist"], Icon)
            notify.show()             

    client.disconnect()
    sys.exit(0)

# Script starts here
if __name__ == "__main__":
    main()