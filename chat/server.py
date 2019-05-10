#!/usr/bin/env python3
import socket
import threading
from time import sleep

max_len_data = 1024

def server_init( host, port ):
    print( "start server in %s:%i"%(host, port) )
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    server.bind( (host, port) )
    server.listen(100)
    #client, addr = server.accept()
    return server

def session( users, user, client ):

    t = '`%s` login\n'%user + 'Online users: ' + ','.join( list(users.keys()) )
    for u in users.keys():
        users[u][0].send( t.encode( 'utf-8' ) )

    while True:
        recv = client.recv(max_len_data).decode( 'utf-8' )
        send = '%s: '%user + recv

        if recv == 'session_close':
            send = '%s: exit'%user

        for u in users.keys():
            if u == user:
                continue
            users[u][0].send( send.encode( 'utf-8' ) )

        if recv == 'session_close':
            print( 'user `%s` exit'%user )
            del( users[user] )
            break
    client.close()



def new_session( users, client, addr ):
    #print( 'users: ', users.keys() )
    while True:
        user = client.recv( max_len_data ).decode( 'utf-8' )
        if user == 'session_close':
            client.close()
            return
        if user in users.keys():
            client.send( 'Failed'.encode( 'utf-8' ) )
        else:
            client.send( 'Ok'.encode( 'utf-8' ) )
            break

    print( 'user: `%s` login'%user )
    #print( 'user: %s, password: %s'%(user,password) )

    t = threading.Thread( target=session, args=(users, user, client) )
    users[user] = [ client, addr, t ]
    print( 'online users: ', list(users.keys()) )
    t.start()

def main():
    host = 'localhost'
    port = int( input('port: ') )
    server = server_init( host, port )

    users = {}

    while True:
        client, addr = server.accept()
        new_session( users, client, addr )

    server.close()

if __name__ == '__main__': main()
