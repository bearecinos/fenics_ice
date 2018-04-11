import sys
sys.path.insert(0,'../code/')
from fenics import *
from dolfin import *
import model
import solver
import matplotlib.pyplot as plt
import numpy as np
import fenics_util as fu
import time
import datetime
import pickle
from IPython import embed

set_log_level(20)

#Load Data
dd = './output_smith_inv/'
param = pickle.load( open( ''.join([dd,'param.p']), "rb" ) )
param['outdir'] = './output_smith_forward/'

data_mesh = Mesh(''.join([dd,'data_mesh.xml']))
M_dm = FunctionSpace(data_mesh,'DG',0)
data_mask = Function(M_dm,''.join([dd,'data_mask.xml']))

mdl_mesh = Mesh(''.join([dd,'mesh.xml']))

V = VectorFunctionSpace(mdl_mesh,'Lagrange',1,dim=2)
Q = FunctionSpace(mdl_mesh,'Lagrange',1)
M = FunctionSpace(mdl_mesh,'DG',0)

U = Function(V,''.join([dd,'U.xml']))
alpha = Function(Q,''.join([dd,'alpha.xml']))
beta = Function(Q,''.join([dd,'beta.xml']))
bed = Function(Q,''.join([dd,'bed.xml']))
surf = Function(Q,''.join([dd,'surf.xml']))
thick = Function(M,''.join([dd,'thick.xml']))
mask = Function(M,''.join([dd,'mask.xml']))
mask_vel = Function(M,''.join([dd,'mask_vel.xml']))
u_obs = Function(M,''.join([dd,'u_obs.xml']))
v_obs = Function(M,''.join([dd,'v_obs.xml']))
u_std = Function(M,''.join([dd,'u_std.xml']))
v_std = Function(M,''.join([dd,'v_std.xml']))
uv_obs = Function(M,''.join([dd,'uv_obs.xml']))
Bglen = Function(M,''.join([dd,'Bglen.xml']))
B2 = Function(Q,''.join([dd,'B2.xml']))


param['run_length'] =  10.0
param['n_steps'] = 120

mdl = model.model(data_mesh,data_mask, param)
mdl.init_bed(bed)
mdl.init_thick(thick)
mdl.gen_surf()
mdl.init_mask(mask)
mdl.init_vel_obs(u_obs,v_obs,mask_vel,u_std,v_std)
mdl.init_lat_dirichletbc()
mdl.init_bmelt(Constant(0.0))
mdl.init_alpha(alpha)
mdl.init_beta(beta)
mdl.label_domain()

#Solve
slvr = solver.ssa_solver(mdl)
slvr.timestep(save=1, adjoint_flag=0, outdir=param['outdir'])

embed()

#Balance melt rates
hdf = HDF5File(slvr.mesh.mpi_comm(), param['outdir'] + 'H_ts.h5', "r")
attr = hdf.attributes("H")
nsteps = attr['count']

dt= param['run_length']/param['n_steps']

iter_s = np.ceil(5.0/dt)  #Iteration closest to 5yr
iter_f = nsteps - 1         #Final iteration
dT = dt*(iter_f - iter_s) #Time diff in years between iterations

HS = Function(slvr.M)
HF = Function(slvr.M)
hdf.read(HS, "H/vector_{0}".format(int(iter_s)))
hdf.read(HF, "H/vector_{0}".format(int(iter_f)))

H_s = -param['rhow']/param['rhoi'] * bed
fl_ex = conditional(slvr.H_init <= H_s, Constant(1.0), Constant(0.0))

dHdT = project(fl_ex*(HF - HS)/dT, slvr.M)
Function.set_allow_extrapolation(dHdT, True)
dHdT_dm = project(dHdT, M_dm)

outdir = mdl.param['outdir']
vtkfile = File(''.join([outdir,'dHdT_dm.pvd']))
xmlfile = File(''.join([outdir,'dHdT_dm.xml']))
vtkfile << dHdT_dm
xmlfile << dHdT_dm


#slvr.set_J_vaf()
#slvr.comp_dJ_vaf(mdl.alpha)
#plot(slvr.dJ_vaf)
#plt.savefig('tmp.png')


#Output model variables in ParaView+Fenics friendly format
outdir = mdl.param['outdir']
pickle.dump( mdl.param, open( ''.join([outdir,'param.p']), "wb" ) )

File(''.join([outdir,'mesh.xml'])) << mdl.mesh
File(''.join([outdir,'data_mesh.xml'])) << data_mesh

vtkfile = File(''.join([outdir,'dJ_vaf.pvd']))
xmlfile = File(''.join([outdir,'dJ_vaf.xml']))
vtkfile << slvr.dJ_vaf
xmlfile << slvr.dJ_vaf

vtkfile = File(''.join([outdir,'U.pvd']))
xmlfile = File(''.join([outdir,'U.xml']))
vtkfile << slvr.U
xmlfile << slvr.U

vtkfile = File(''.join([outdir,'beta.pvd']))
xmlfile = File(''.join([outdir,'beta.xml']))
vtkfile << slvr.beta
xmlfile << slvr.beta

vtkfile = File(''.join([outdir,'bed.pvd']))
xmlfile = File(''.join([outdir,'bed.xml']))
vtkfile << mdl.bed
xmlfile << mdl.bed

vtkfile = File(''.join([outdir,'thick.pvd']))
xmlfile = File(''.join([outdir,'thick.xml']))
H = project(mdl.H, mdl.M)
vtkfile << H
xmlfile << H

vtkfile = File(''.join([outdir,'mask.pvd']))
xmlfile = File(''.join([outdir,'mask.xml']))
vtkfile << mdl.mask
xmlfile << mdl.mask

vtkfile = File(''.join([outdir,'data_mask.pvd']))
xmlfile = File(''.join([outdir,'data_mask.xml']))
vtkfile << mask
xmlfile << mask

vtkfile = File(''.join([outdir,'mask_vel.pvd']))
xmlfile = File(''.join([outdir,'mask_vel.xml']))
vtkfile << mdl.mask_vel
xmlfile << mdl.mask_vel

vtkfile = File(''.join([outdir,'u_obs.pvd']))
xmlfile = File(''.join([outdir,'u_obs.xml']))
vtkfile << mdl.u_obs
xmlfile << mdl.u_obs

vtkfile = File(''.join([outdir,'v_obs.pvd']))
xmlfile = File(''.join([outdir,'v_obs.xml']))
vtkfile << mdl.v_obs
xmlfile << mdl.v_obs

vtkfile = File(''.join([outdir,'u_std.pvd']))
xmlfile = File(''.join([outdir,'u_std.xml']))
vtkfile << mdl.u_std
xmlfile << mdl.u_std

vtkfile = File(''.join([outdir,'v_std.pvd']))
xmlfile = File(''.join([outdir,'v_std.xml']))
vtkfile << mdl.v_std
xmlfile << mdl.v_std

vtkfile = File(''.join([outdir,'uv_obs.pvd']))
xmlfile = File(''.join([outdir,'uv_obs.xml']))
U_obs = project((mdl.v_obs**2 + mdl.u_obs**2)**(1.0/2.0), mdl.M)
vtkfile << U_obs
xmlfile << U_obs

vtkfile = File(''.join([outdir,'alpha.pvd']))
xmlfile = File(''.join([outdir,'alpha.xml']))
vtkfile << mdl.alpha
xmlfile << mdl.alpha

vtkfile = File(''.join([outdir,'Bglen.pvd']))
xmlfile = File(''.join([outdir,'Bglen.xml']))
Bglen = project(exp(mdl.beta),mdl.M)
vtkfile << Bglen
xmlfile << Bglen

vtkfile = File(''.join([outdir,'B2.pvd']))
xmlfile = File(''.join([outdir,'B2.xml']))
vtkfile << B2
xmlfile << B2

vtkfile = File(''.join([outdir,'surf.pvd']))
xmlfile = File(''.join([outdir,'surf.xml']))
vtkfile << mdl.surf
xmlfile << mdl.surf


embed()
