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

def make_data( s, h=0 ):
    if len(s) == 0:
        s = ' '
    r = '%i%s'%(h,s)
    return r

def get_data( s ):
    if len(s) == 1:
        s += ' '
    return ( s[0], s[1:] )

def session( users, user, client ):

    t = '`%s` login\n'%user + 'Online users: ' + ','.join( list(users.keys()) )
    t = make_data( t, 1 )
    for u in users.keys():
        users[u][0].send( t.encode( 'utf-8' ) )

    while True:
        recv = client.recv(max_len_data).decode( 'utf-8' )
        h, recv = get_data( recv )
        send = '%s: '%user + recv
        send = make_data( send )


        for u in users.keys():
            if h == '2':
                continue
            #if u == user:
            #    continue
            users[u][0].send( send.encode( 'utf-8' ) )

        if h == '2':
            print( 'user `%s` logout'%user )
            del( users[user] )
            print( 'online users: ', list(users.keys()) )

            t = '`%s` logout\n'%user + 'Online users: ' + ','.join( list(users.keys()) )
            t = make_data( t, 1 )
            for u in users.keys():
                users[u][0].send( t.encode( 'utf-8' ) )
            break
    client.close()



def new_session( users, client, addr ):
    #print( 'users: ', users.keys() )
    while True:
        data = client.recv( max_len_data ).decode( 'utf-8' )
        h, user = get_data( data )
        if h == '2':
            client.close()
            return
        if user in users.keys():
            t = make_data( ' ', 4 )
            client.send( t.encode( 'utf-8' ) )
        else:
            t = make_data( ' ', 3 )
            client.send( t.encode( 'utf-8' ) )
            break

    print( 'user: `%s` login'%user )
    #print( 'user: %s, password: %s'%(user,password) )

    users[user] = [ client,  addr, t ]
    sleep(1)
    t = threading.Thread( target=session, args=(users, user, client) )
    print( 'online users: ', list(users.keys()) )
    t.start()

def main():
    address = input('address: ')
    host,port = address.split( ':' )
    port = int(port)
    server = server_init( host, port )

    users = {}

    while True:
        client, addr = server.accept()
        new_session( users, client, addr )

    server.close()

if __name__ == '__main__':
    main()
