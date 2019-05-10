#!/usr/bin/env python3
import socket
import threading
import curses
from time import sleep

max_len_data = 1024
class windows():

    def __init__(self):

        self.stdscr = curses.initscr()

        curses.echo()
        curses.start_color()
        curses.use_default_colors()

        self.stdscr.clear()
        self.stdscr.scrollok( True )
        self.ymax, self.xmax = self.stdscr.getmaxyx()

        self.create_login_win()

        self.output_pos = 0

    def create_login_win(self):

        self.win_login_width = 36
        self.win_login = curses.newwin( 3, self.win_login_width, self.ymax//2-1,\
                self.xmax//2-self.win_login_width//2 )
        self.win_login.border()
        self.init_single_win( self.win_login, 'server' )
        self.win_login.addstr( 1, 1, '[IP:port]:' )
        self.win_login.refresh()

    def server_err(self):
        self.init_single_win( self.win_login, 'server' )
        self.win_login.addstr( 1, 1, 'server is closed', curses.A_BLINK )
        self.win_login.refresh()
        sleep(2)

    def get_server(self):
        self.server = self.win_login.getstr( 1, 12, self.win_login_width-12-2 ).decode('utf-8')
        return self.server

    def get_input(self):
        y,x  = self.win_input.getmaxyx()
        r = self.win_input.getstr( 1, 1, x-2 ).decode('utf-8')
        self.reset_win_input()
        return r

    def get_username(self):
        self.init_single_win( self.win_login, 'username' )
        self.username = self.win_login.getstr( 1, 1, self.win_login_width ).decode('utf-8')
        return self.username

    def reget_username(self):
        self.win_login.addstr( 1, 1, '`%s` exist!'%self.username, curses.A_BLINK)
        self.win_login.refresh()
        sleep(2)
        self.init_single_win( self.win_login, 'username' )
        self.username = self.win_login.getstr( 1, 1, self.win_login_width ).decode('utf-8')
        return self.username

    def create_chat_win(self):

        self.win_login.clear()

        self.height_input = 3
        self.height_list = 5
        self.height_output = self.ymax - self.height_input - self.height_list

        self.win_list = curses.newwin( self.height_list, 0, 0, 0 )
        self.init_single_win( self.win_list, 'list' )

        self.win_output = curses.newwin( self.height_output, 0, self.height_list, 0 )
        self.init_single_win( self.win_output, 'output' )

        self.win_input = curses.newwin( self.height_input, 0, self.height_output+self.height_list, 0 )
        self.init_single_win( self.win_input, 'input' )

    def close(self):
        curses.endwin()

    def init_single_win( self, win, title ):
        win.clear()
        win.border()
        #y,x = win.getmaxyx()
        #win.addstr( 0, (x-len(title))//2, title )
        win.addstr( 0, 1, title )
        win.refresh()

    def reset_win_input( self ):
        self.init_single_win( self.win_input, 'input' )

    def reset_win_login( self ):
        self.init_single_win( self.win_longin, 'server' )

    def reset_win_output( self ):
        self.init_single_win( self.win_output, 'output' )

    def win_list_clear( self ):
        self.init_single_win( self.win_list, 'list' )

    def output( self, s ):
        s = s.split( '\n' )
        y, x = self.win_output.getmaxyx()
        x = x-2
        for ss in s:
            l = len(ss)
            while l>x:
                self.output_pos += 1
                if self.output_pos ==  y-1:
                    self.output_pos = 1
                    self.reset_win_output() # should be scrolling

                self.win_output.addstr( self.output_pos, 1, ss[:x] )
                ss = ss[x:]
                l = len(ss)
            if len(ss) > 0:
                self.output_pos += 1
                if self.output_pos ==  y-1:
                    self.output_pos = 1
                    self.reset_win_output() # should be scrolling

                self.win_output.addstr( self.output_pos, 1, ss )

        self.win_output.refresh()

    def output_list( self, s ):
        n = 1
        self.win_list_clear()
        s = s.split( '\n' )
        for ss in s:
            self.win_list.addstr( n, 1, ss )
            n += 1
            if n ==  self.height_list:
                n = 1
                self.reset_win_list() # should be scrolling
        self.win_list.refresh()


def make_data( s, h=0 ):
    if len(s) == 0:
        s = ' '
    r = '%i%s'%(h,s)
    return r

def get_data( s ):
    if len(s) == 1:
        s += ' '
    return (s[0], s[1:])

def my_recv( client, wins ):
    while True:
        recv = ''
        try:
            recv = client.recv( max_len_data ).decode( 'utf-8' )
        except OSError:
            return
        if len(recv) != 0:
            h, recv = get_data( recv )
            if h == '0':
                wins.output( recv )
            if h == '1':
                wins.output_list( recv )


def main():

    wins = windows()

    address = wins.get_server()

    host,port = address.split( ':' )
    port = int(port)
    client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    try:
        client.connect( (host,port) )
    except ConnectionRefusedError:
        client.close()
        wins.server_err()
        wins.close()
        exit()


    username = wins.get_username()
    while True:
        if username == 'q':
            wins.close()
            client.close()
            exit()
        username = make_data( username )
        client.send( username.encode( 'utf-8' ) )
        data = client.recv( wins.xmax-2 ).decode( 'utf-8' )
        h, r = get_data( data )

        if h == '3':
            break

        username = wins.reget_username()

    wins.create_chat_win()

    t = threading.Thread( target=my_recv, args=(client, wins) )
    t.start()

    while True:

        send = wins.get_input()
        if send == 'q':
            send = make_data( ' ', 2 )
            client.send( send.encode( 'utf-8' ) )
            break
        send = make_data( send )
        client.send( send.encode( 'utf-8' ) )
        #wins.output( send )

    client.close()
    curses.endwin()



if __name__ == '__main__':
    main()
