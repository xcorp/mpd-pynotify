#!/usr/bin/python


# IMPORTS
import sys, os
import pynotify
import mpd
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  


Tune=os.path.join(os.path.split(__file__)[0], 'Tune.png')
Play=os.path.join(os.path.split(__file__)[0], 'Play.png')
Pause=os.path.join(os.path.split(__file__)[0], 'Pause.png')
Stop=os.path.join(os.path.split(__file__)[0], 'Stop.png')
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
    if not mpdConnect(client, CON_ID):
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
            
    prevsong=client.playlistinfo()[int(client.status()['song'])]
    prevstate=client.status()['state']
    while True:     
        client.idle('player')
        currsong=client.playlistinfo()[int(client.status()['song'])]
        currstate=client.status()['state']
        if not prevstate == currstate:
            prevstate = currstate
            if currstate == 'play':
                Icon = Play
            elif currstate == 'pause':
                Icon = Pause
            elif currstate == 'stop':
                Icon = Stop
            else:
                Icon = Tune
        if not prevsong == currsong:
            prevsong = currsong
            Icon = Tune
        notify.update(client.playlistinfo()[int(client.status()['song'])]['title'],client.playlistinfo()[int(client.status()['song'])]["artist"], Icon)
        notify.show()             
        
    client.disconnect()
    sys.exit(0)

# Script starts here
if __name__ == "__main__":
    main()