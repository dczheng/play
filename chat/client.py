#!/usr/bin/env python3
import socket
import threading
import sys
import os

max_len_data = 1024
address = input( 'server: ' )
host,port = address.split( ':' )
port = int(port)
client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
try:
    client.connect( (host,port) )
except ConnectionRefusedError:
    print( 'server is closed!' )
    client.close()
    exit()

print( "connect to %s"%address )

#if input( 'Creat Account? (N/y)' ) == 'y':
#    pass
#else:
#    #username = input( "username: " )
#    #password = input( "password: " )
#    send = "%s+%s"%(username,password)
#    client.send( send.encode( 'utf-8' ) )

while True:
    username = input( "username: " )
    if username == 'q':
        client.send( 'session_close'.encode( 'utf-8' ) )
        exit()
    client.send( username.encode( 'utf-8' ) )
    r = client.recv( max_len_data ).decode( 'utf-8' )
    if r == 'Ok':
        break
    print( '%s exist!'%username )

def my_recv( client ):
    while True:
        try:
            recv = client.recv( max_len_data ).decode( 'utf-8' )
        except OSError:
            return
        print( '\r' + recv + '\nme: ', end='' )


t = threading.Thread( target=my_recv, args=(client,) )
t.start()

while True:

    send = input( 'me: ' )
    if send == 'q':
        client.send( 'session_close'.encode( 'utf-8' ) )
        break
    client.send( send.encode( 'utf-8' ) )

client.close()
