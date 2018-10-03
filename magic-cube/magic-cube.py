#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import random

class magic_cube:

    def __init__( self ):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot( 111, projection='3d' )
        '''
        self.ax.set_xticks( [] )
        self.ax.set_yticks( [] )
        self.ax.set_zticks( [] )
        '''

        self.ax.set_axis_off()
        self.ax.set_aspect( 'equal' )
        self.fig.set_facecolor( 'k' )
        self.ax.set_facecolor( 'k' )

        self.color = [ 'r', 'w', 'c', 'g', 'y', 'm' ]
        self.edge_color = 'k'

        self.color_list = []

        self.coor_min_max = [0, 1]

        for i in range( 6 ):
            self.color_list += self.color[i] * 9

        #random.shuffle( self.color_list )
        #print( self.color_list )

        self.P_coor = []

        for i in range( 6 ):
            self.P_coor.append( [] )

        for l in range( 6 ):
            C2 = self.gen_c2();
            shift_n = l // 2
            for i in range( 9 ):
                t = C2[i]
                for ti in range( 4 ):
                    t[ti].append( self.coor_min_max[l%2] )
                    t[ti] = t[ti][shift_n:] + t[ti][:shift_n]
                self.P_coor[l].append( t )

        #print( self.P_coor[0][0] )

    def rotate( self, index, ang ):

        ang = ang / 180.0 * np.pi

        s = np.sin( ang )
        c = np.cos( ang )

        index_1 = index % 10
        index_2 = index // 10

        if index_1 == 1:   # around x
            mat = [
                    [ 1, 0,  0],
                    [ 0, c, -s],
                    [ 0, s,  c]
                  ]
        if index_1 == 2:   # around y
            mat = [
                    [ c, 0, -s],
                    [ 0, 1,  0],
                    [ s, 0,  c]
                  ]
        if index_1 == 3:   # around z
            mat = [
                    [ c, -s, 0 ],
                    [ s,  c, 0 ],
                    [ 0,  0, 1 ]
                  ]

        p = []

        #continue in next time

    def gen_c2( self ):

        x = np.linspace( self.coor_min_max[0], self.coor_min_max[1], 4 )

        C2 = []
        for i in range( 3 ):
            for j in range( 3 ):
                C2.append( [ [ x[i],   x[j]   ],
                             [ x[i],   x[j+1] ],
                             [ x[i+1], x[j+1]   ],
                             [ x[i+1], x[j] ] ] )
        return C2

    def show( self ):

        for l in range( 6 ):
            p_cor  = self.color_list[ l*9:(l+1)*9 ]
            p_coor = self.P_coor[l]
            for i in range( len( p_coor ) ):
                p = p_coor[i]
                x = mplot3d.art3d.Poly3DCollection( [p] )
                x.set_color( p_cor[i] )
                x.set_edgecolor( 'k' )
                self.ax.add_collection3d( x )

        plt.show()



def main():

    mc = magic_cube()

    mc.show()


if __name__ == '__main__':
    main()
