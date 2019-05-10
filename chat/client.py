#!/usr/bin/env python3
import socket
import threading
import curses
from time import sleep

max_len_data = 1024

def my_recv( client, win_s, win_o ):
    n = 1
    while True:
        try:
            recv = client.recv( max_len_data ).decode( 'utf-8' )
        except OSError:
            return
        if len(recv) != 0:
            win_o.addstr( n, 1, recv )
            n += 1
            win_o.refresh()

def create_wins():
    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.scrollok( True )
    ymax, xmax = stdscr.getmaxyx()
    curses.echo()

    curses.start_color()
    curses.use_default_colors()

    height_input = 5
    height_status = 5
    height_output = ymax - height_input - height_status

    win_output = curses.newwin( height_output, 0, 0, 0 )
    win_output.border()
    win_output.addstr( 0, 1, 'output' )
    win_output.refresh()

    win_status = curses.newwin( height_status, 0, height_output, 0 )
    win_status.border()
    win_status.addstr( 0, 1, 'status' )
    win_status.refresh()

    win_input = curses.newwin( height_input, 0, height_output+height_status, 0 )
    win_input.border()
    win_input.addstr( 0, 1, 'input' )
    win_input.refresh()
    return ( win_input, win_status, win_output, stdscr )

def main():

    win_i, win_s, win_o, stdscr = create_wins()

    #address = input( 'server: ' )
    win_i.addstr( 1, 1, 'server:', curses.A_UNDERLINE )
    address = win_i.getstr( 1,9,max_len_data )
    address = address.decode( 'utf-8' )

    host,port = address.split( ':' )
    port = int(port)
    client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    try:
        client.connect( (host,port) )
    except ConnectionRefusedError:

        win_i.addstr( 2, 1, 'server is closed!', curses.A_BLINK )
        win_i.refresh()
        client.close()
        sleep(2)
        curses.endwin()
        exit()

    win_i.addstr( 2, 1, 'connect to %s'%address )
    win_i.refresh()

    while True:
        win_i.addstr( 3, 1, 'username:', curses.A_UNDERLINE )
        username = win_i.getstr( 3,11, max_len_data )
        username = username.decode( 'utf-8' )
        #username = input( "username: " )
        if username == 'q':
            curses.endwin()
            client.close()
            exit()
        client.send( username.encode( 'utf-8' ) )
        r = client.recv( max_len_data ).decode( 'utf-8' )

        if r == 'Ok':
            break

        win_i.addstr( 3, 1, 'username:', curses.A_UNDERLINE )
        win_i.addstr( 3, 11, ' ' * (len(username)+1)  )
        win_i.addstr( 4, 1, '`%s` exist!'%username, curses.A_BLINK)


    t = threading.Thread( target=my_recv, args=(client, win_s, win_o) )
    t.start()

    while True:

        win_i.clear()
        win_i.border()
        win_i.addstr( 0, 1, 'input' )
        win_i.refresh()

        win_i.addstr( 1, 1, 'me:' )
        send = win_i.getstr( 1,5, max_len_data ).decode( 'utf-8' )
        if send == 'q':
            client.send( 'session_close'.encode( 'utf-8' ) )
            break
        client.send( send.encode( 'utf-8' ) )

    client.close()
    curses.endwin()



if __name__ == '__main__':
    main()
