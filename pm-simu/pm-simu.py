#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

class pm_simu:
    def __init__( self, Npart, mass, pos, vel, mesh, time, boxsize, cosmo_para ):
        self.Npart = Npart
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.mesh = mesh
        self.time = time
        self.cosmo = cosmo_para
        self.boxsize = boxsize
        self.nowtime = self.time[0]

        self.check_input()

        self.cell = self.boxsize / self.mesh
        self.vcell = self.cell[0] * self.cell[1] * self.cell[2]
        self.rho = np.zeros( mesh )
        self.acc = np.zeros( [self.Npart, 0] )

    def show_parameters( self ):
        print( "Npart: ", self.Npart )
        print( "mesh:", self.mesh )
        print( "cell:", self.cell )

    def check_input( self ):
        pass

    def calc_rho( self ):
        for i in range( self.Npart ):
            x = int(self.pos[i,0] / self.cell[0])
            y = int(self.pos[i,1] / self.cell[1])
            z = int(self.pos[i,2] / self.cell[2])
            self.rho[ x, y, z ] = self.rho[ x, y, z ] + self.mass[ i ]
        #print( self.rho )

    def save_rho( self ):
        rho = np.sum( self.rho, axis=2 )
        plt.imshow( rho )
        s = "./rho_%08.5f.png"%(self.nowtime)
        print( "Time:%05.2f ---> save rho to %s"%(self.nowtime, s) )
        plt.savefig( s )

    def show_phi( self ):
        phi = np.sum( self.phi, axis=2 )
        plt.imshow( phi )
        plt.show()

    def calc_phi( self ):
        self.rho_k = np.fft.fftn( self.rho )
        kx = np.linspace( 1, self.mesh[0], self.mesh[0] )
        ky = np.linspace( 1, self.mesh[0], self.mesh[0] )
        kz = np.linspace( 1, self.mesh[0], self.mesh[0] )
        KX, KY, KZ = np.meshgrid( kx, ky, kz )
        KX = KX * 2 * np.pi / self.boxsize
        KY = KY * 2 * np.pi / self.boxsize
        KZ = KZ * 2 * np.pi / self.boxsize
        k2 = np.power( KX, 2.0 ) + np.power( KY, 2.0 ) + np.power( KZ, 2.0 )
        self.phi_k = 4 * np.pi * self.rho_k / k2
        self.phi = np.abs(np.fft.ifftn( self.phi_k ))
        #rho_k_2 = np.sum( np.real(rho_k), axis=2 )
        #plt.imshow( rho_k_2 )
        #plt.show()

    def calc_force( self ):
        self.force = np.gradient( self.phi )
        self.force[0] = self.force[0] * self.rho * self.vcell
        self.force[1] = self.force[1] * self.rho * self.vcell
        self.force[2] = self.force[2] * self.rho * self.vcell

    def move_particle( self ):
        for i in range( self.Npart ):
            #print( self.pos[i,0], self.pos[i,1], self.pos[i,2] )
            x = int(self.pos[i,0] / self.cell[0])
            y = int(self.pos[i,1] / self.cell[1])
            z = int(self.pos[i,2] / self.cell[2])
            #print( x, y, z )
            acc_x = self.force[0][x,y,z] / self.mass[i]
            acc_y = self.force[1][x,y,z] / self.mass[i]
            acc_z = self.force[2][x,y,z] / self.mass[i]
            self.vel[i, 0] += acc_x * self.time[2]
            self.vel[i, 1] += acc_y * self.time[2]
            self.vel[i, 2] += acc_z * self.time[2]
            self.pos[i, 0] += self.vel[i,0] * self.time[2]
            self.pos[i, 1] += self.vel[i,1] * self.time[2]
            self.pos[i, 2] += self.vel[i,2] * self.time[2]
            while self.pos[i,0] > self.boxsize: self.pos[i,0] -= self.boxsize
            while self.pos[i,1] > self.boxsize: self.pos[i,1] -= self.boxsize
            while self.pos[i,2] > self.boxsize: self.pos[i,2] -= self.boxsize
            while self.pos[i,0] < 0: self.pos[i,0] += self.boxsize
            while self.pos[i,1] < 0: self.pos[i,1] += self.boxsize
            while self.pos[i,2] < 0: self.pos[i,2] += self.boxsize

    def calc_timestep( self ):
        pass

    def do_simu( self ):
        while( self.nowtime < self.time[1] ):
            self.calc_rho()
            self.save_rho()
            self.calc_phi()
            #self.show_phi()
            self.calc_force()
            self.move_particle()
            self.calc_timestep()
            self.nowtime += self.time[2]

def main():
    N = 1000000
    mesh = np.array( [100, 100, 100] )
    mass = np.ones( N )
    boxsize = 50
    pos = np.random.uniform( 0, 49, N*3 )
    pos = pos.reshape( [N,3] )
    vel = np.random.uniform( 0, 0.2, N*3 )
    vel = vel.reshape( [N,3] )
    time = np.array( [0, 10, 0.1] )
    #print( pos )
    #print( vel )
    test = pm_simu( N, mass, pos, vel, mesh, time, boxsize, None )
    test.show_parameters()
    test.do_simu()

    #print( m )


if __name__ ==  '__main__':
    main()
