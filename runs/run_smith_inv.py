import sys
sys.path.insert(0,'../code/')
from fenics import *
import model
import solver
import matplotlib.pyplot as plt
import numpy as np
import fenics_util as fu
import time
import datetime
import pickle
from IPython import embed

#Store key python variables in here
savefile = 'smithinv_' + datetime.datetime.now().strftime("%m%d%H%M")

set_log_level(20)

#Load Data
dd = '../input/smith_500m_input/'
data_mesh = Mesh(''.join([dd,'smith450m_mesh.xml']))
Q = FunctionSpace(data_mesh, 'DG', 0)
bed = Function(Q,''.join([dd,'smith450m_mesh_bed.xml']), name = "bed")
thick = Function(Q,''.join([dd,'smith450m_mesh_thick.xml']), name = "thick")
mask = Function(Q,''.join([dd,'smith450m_mesh_mask.xml']), name = "mask")
u_obs = Function(Q,''.join([dd,'smith450m_mesh_u_obs.xml']), name = "u_obs")
v_obs = Function(Q,''.join([dd,'smith450m_mesh_v_obs.xml']), name = "v_obs")
u_std = Function(Q,''.join([dd,'smith450m_mesh_u_std.xml']), name = "u_std")
v_std = Function(Q,''.join([dd,'smith450m_mesh_v_std.xml']), name = "v_std")
mask_vel = Function(Q,''.join([dd,'smith450m_mesh_mask_vel.xml']), name = "mask_vel")
B_mod = Function(Q,''.join([dd,'smith450m_mesh_mask_B_mod.xml']), name = "B_mod")

#Generate model mesh
gf = 'grid_data.npz'
npzfile = np.load(''.join([dd,'grid_data.npz']))
nx = int(npzfile['nx'])
ny = int(npzfile['ny'])
xlim = npzfile['xlim']
ylim = npzfile['ylim']

mesh = RectangleMesh(Point(xlim[0],ylim[0]), Point(xlim[-1], ylim[-1]), nx, ny, 'crossed')

#Initialize Model
param = {'eq_def' : 'weak',
        'solver': 'petsc',
        'outdir' :'./output_smith_inv_reg2/',
        'gc1': 1.0, #1e2
        'gc2': 0.0, #1e0
        'gr1': 1e2, #1e1
        'gr2': 1e4,#1e5
        'gr3': 1e0,#1e1
        }
def forward(alpha = None):
    mdl = model.model(mesh,mask, param)
    mdl.init_bed(bed)
    mdl.init_thick(thick)
    mdl.gen_surf()
    mdl.init_mask(mask)
    mdl.init_vel_obs(u_obs,v_obs,mask_vel,u_std,v_std)
    mdl.init_lat_dirichletbc()
    mdl.init_bmelt(Constant(0.0))
    if alpha is None:
        mdl.gen_alpha()
        #mdl.init_alpha(Constant(ln(6000))) #Initialize using uniform alpha
        alpha = mdl.alpha
    else:
        mdl.init_alpha(alpha)
    mdl.init_beta(ln(B_mod))            #Comment to use uniform Bglen

    mdl.label_domain()

    #Solve
    slvr = solver.ssa_solver(mdl)
    slvr.def_mom_eq()
    slvr.solve_mom_eq()

    return alpha, mdl, slvr

alpha0, mdl, slvr = forward()

from dolfin_adjoint import *
parameters["adjoint"]["stop_annotating"] = True
adj_html("forward.html", "forward")

#embed()
# cc = Control(alpha0)
# u,v = split(slvr.U)
# J_ls = (mdl.u_std**(-2)*(u-mdl.u_obs)**2 + mdl.v_std**(-2)*(v-mdl.v_obs)**2)*slvr.dObs
# #dJ_ls = compute_gradient(Functional(J_ls), cc, forget = False)
# def J_ls_test(alpha):
#     _, mdl, slvr = forward(alpha)
#     u,v = split(slvr.U)
#     J_ls = (mdl.u_std**(-2)*(u-mdl.u_obs)**2 + mdl.v_std**(-2)*(v-mdl.v_obs)**2)*slvr.dObs
#     return assemble(J_ls)
# #minconv = taylor_test(J_ls_test, cc, assemble(J_ls), dJ_ls, seed = 1.0e-7, size = 2)
# hess = hessian(Functional(J_ls),cc)
# direction = interpolate(Constant(1), alpha0.function_space())
# hess( direction)
# import sys;  sys.exit(0)

#Inversions
slvr.inversion()

#Plots for quick output evaluation
B2 = project(exp(slvr.alpha),mdl.Q)
F_vals = [x for x in slvr.F_vals if x > 0]

fu.plot_variable(B2, 'B2', mdl.param['outdir'])
fu.plot_inv_conv(F_vals, 'convergence', mdl.param['outdir'])


#Output model variables in ParaView+Fenics friendly format
outdir = mdl.param['outdir']

File(''.join([outdir,'mesh.xml'])) << data_mesh

vtkfile = File(''.join([outdir,'U.pvd']))
vtkfile << slvr.U

vtkfile = File(''.join([outdir,'beta.pvd']))

vtkfile << slvr.beta

vtkfile = File(''.join([outdir,'bed.pvd']))
vtkfile << mdl.bed

vtkfile = File(''.join([outdir,'thick.pvd']))
vtkfile << mdl.thick

vtkfile = File(''.join([outdir,'mask.pvd']))
vtkfile << mdl.mask

vtkfile = File(''.join([outdir,'mask_ext.pvd']))
vtkfile << mdl.mask_ext

vtkfile = File(''.join([outdir,'mask_vel.pvd']))
vtkfile << mdl.mask_vel

vtkfile = File(''.join([outdir,'u_obs.pvd']))
vtkfile << mdl.u_obs

vtkfile = File(''.join([outdir,'v_obs.pvd']))
vtkfile << mdl.v_obs

vtkfile = File(''.join([outdir,'u_std.pvd']))
vtkfile << mdl.u_std

vtkfile = File(''.join([outdir,'v_std.pvd']))
vtkfile << mdl.v_std

vtkfile = File(''.join([outdir,'uv_obs.pvd']))
U_obs = project((mdl.v_obs**2 + mdl.u_obs**2)**(1.0/2.0), mdl.M)
vtkfile << U_obs

vtkfile = File(''.join([outdir,'alpha.pvd']))
vtkfile << mdl.alpha

vtkfile = File(''.join([outdir,'Bglen.pvd']))
Bglen = project(exp(mdl.beta),mdl.M)
vtkfile << Bglen

vtkfile = File(''.join([outdir,'B2.pvd']))
vtkfile << B2

vtkfile = File(''.join([outdir,'surf.pvd']))
vtkfile << mdl.surf

embed()
