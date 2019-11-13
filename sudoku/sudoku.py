#!/usr/bin/env python3

import os 
import time

class sudoku:

    def __init__( self, fn ):
        
        self.S = open( fn ).readlines()
        self.N = int(self.S[0])
        self.sep = '-' * 20
        del( self.S[0] )
        for i in range( self.N ):
            t = [ int(j) for j in self.S[i].split() ]
            self.S[i] = t

        self.SS = []

        for i in range( self.N ):
            for j in range( self.N ):
                v = self[i,j]
                if v != 0:
                    self.SS.append( [v] )
                else:
                    self.SS.append( self.find_number( i, j ) )
        self.print_sep( 'origin' )
        print( self )
        for i in range( self.N * self.N ):
            if len(self.SS[i]) == 1:
                self[i//self.N, i%self.N] = self.SS[i][0]
        self.print_sep( 'initial' )
        print( self )

    def print_sep( self, s ):
        print( self.sep )
        print( '%s:'%s )

    def print_test( self ):
        for i in range( self.N * self.N ):
            print( self.SS[i], end='' )
            if i % self.N == self.N-1:
                print()

    def find_number( self, ii, jj ):
        r = []
        for i in range( 1, self.N + 1 ):
            if ( not i in self[ii,:] ) and ( not i in self[:, jj] ):
                r.append( i )
        return r

    def __getitem__( self, index ):

        if isinstance( index[0], slice ) and isinstance( index[1], slice ):
            print( 'index error' )
            exit()

        if isinstance( index[0], slice ):
            return [ t[index[1]] for t in self.S[index[0]] ]

        if isinstance( index[1], slice ):
            return self.S[index[0]][index[1]]
        return self.S[index[0]][index[1]]

    def __setitem__( self, index, v ):
        if isinstance( index[0], slice ) or isinstance( index[1], slice ):
            print( 'index error' )
            exit()
        self.S[index[0]][index[1]] = v

    def __str__( self ):
        #os.system( "clear" )
        #r = "N: %i\n"%self.N
        r = ''
        for i in range( self.N ):
            for j in range( self.N ):
                r = r + "%i "%(self[i, j])
            r = r + '\n'
        #self.print_test()
        r = r + self.sep
        return r

    def check_final(self):
        #print( 'final' )
        #print( self )
        for i in range( self.N ):
            for j in range( 1, self.N+1 ):
                if (not j in self[i,:]) or ( not j in self[:,i] ):
                    return False
        return True

    def check( self, ii, jj, v ):
        # add extra rules in this function
        if ( v in self[ii,:] ) or ( v in self[:,jj] ):
            return False
        return True

    def solve(self):
        if self._solve( 0 ):
            self.print_sep( 'final' )
            print( self )
            return
        print( "can not solve!" )

    def _solve( self, l ):
        ii = l // self.N
        jj = l % self.N

        #print( l )
        #print( self )

        if self[ii, jj] != 0:
            if l == self.N * self.N - 1:
                if self.check_final():
                    return True
            return self._solve( l+1 )

        for v in self.SS[l]:
            if not self.check( ii, jj, v ):
                continue

            self[ii,jj] = v
            if l == self.N * self.N - 1:
                if self.check_final():
                    return True
            else:
                if self._solve( l+1 ):
                    return True
            self[ii, jj] = 0

        return False

import sys

s = sudoku( sys.argv[1] )
t0 = time.time()
s.solve()
t1 = time.time()
print( "Time: %gs"%( t1-t0 ) )
