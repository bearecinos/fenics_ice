from fenics import *

import numpy as np
import sys
import os
from pylab import plt
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from fenics import *
from IPython import embed
import model
import argparse


def main(dd,noise_sdev, bflag, L):

    data_mesh = Mesh(os.path.join(dd,'mesh.xml'))

    if bflag:
        V = VectorFunctionSpace(data_mesh, 'Lagrange', 1, dim=2, constrained_domain=model.PeriodicBoundary(40e3))
    else:
        V = VectorFunctionSpace(data_mesh, 'Lagrange', 1, dim=2)

    M = FunctionSpace(data_mesh, 'DG', 0)

    U = Function(V,os.path.join(dd,'U.xml'))
    N = Function(M)

    uu,vv = U.split(True)
    u = project(uu,M)
    v = project(vv,M)

    u_array = u.vector().get_local()
    v_array = v.vector().get_local()

    u_noise = np.random.normal(scale=noise_sdev, size=u_array.size)
    v_noise = np.random.normal(scale=noise_sdev, size=v_array.size)

    u.vector().set_local(u.vector().get_local() + u_noise)
    v.vector().set_local(v.vector().get_local() + v_noise)


    File(os.path.join(dd,'data_mesh.xml')) << data_mesh

    xmlfile = File(os.path.join(dd,'u_obs.xml'))
    xmlfile << u
    xmlfile = File(os.path.join(dd,'v_obs.xml'))
    xmlfile << v

    N.assign(Constant(noise_sdev))
    xmlfile = File(os.path.join(dd,'u_std.xml'))
    xmlfile << N

    xmlfile = File(os.path.join(dd,'v_std.xml'))
    xmlfile << N

    N.assign(Constant(1.0))
    xmlfile = File(os.path.join(dd,'mask_vel.xml'))
    xmlfile << N




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datadir', dest='dd', type=str, required=True, help='Directory with input data')
    parser.add_argument('-s', '--sigma', dest='noise_sdev', type=float,  help = 'Standard deviation of added Gaussian Noise')
    parser.add_argument('-b', '--boundaries', dest='bflag', action='store_true', help='Periodic boundary conditions')
    parser.add_argument('-L', '--length', dest='L', type=int, help='Length of IsmipC domain.')

    parser.set_defaults(noise_sdev = 1.0, bflag = False, L = False)
    args = parser.parse_args()

    dd = args.dd
    noise_sdev = args.noise_sdev
    bflag = args.bflag
    L = args.L

    if bflag and not L:
        print('Periodic boundary conditions requiring specifying the domain length with -L')
        raise SystemExit


    main(dd, noise_sdev, bflag, L)

