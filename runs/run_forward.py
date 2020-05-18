import sys
import os

import argparse
from fenics import *
from tlm_adjoint_fenics import *

from fenics_ice import model, solver, inout
from fenics_ice import mesh as fice_mesh
from fenics_ice.config import ConfigParser
import fenics_ice.fenics_util as fu

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import logging as log
from IPython import embed

stop_annotating()

def run_forward(config_file):

    #Read run config file
    params = ConfigParser(config_file)
    inout.setup_logging(params)

    log.info("\n\n==================================")
    log.info("==  RUNNING FORWARD MODEL PHASE ==")
    log.info("==================================\n\n")

    #TODO - issue here - run_inv might need to use 'nx,ny' but run_forward should
    #read mesh...
    #Furthermore - previously this worked by feeding different 'input' & 'output' dir
    #to each stage (run_inv, run_forward, run_errorprop, etc). This should be fixed.


    dd = params.io.input_dir
    outdir = params.io.output_dir

    # Determine Mesh

    #TODO - generalize/improve
    mesh = Mesh(os.path.join(outdir, 'mesh.xml'))

    #data_mesh = fice_mesh.get_data_mesh(params)
    data_mesh = mesh

    # Define Function Spaces
    M = FunctionSpace(mesh, 'DG', 0)
    Q = FunctionSpace(mesh, 'Lagrange', 1)

    # Make necessary modification for periodic bc
    if params.mesh.periodic_bc:
        Qp = fice_mesh.get_periodic_space(params, mesh, dim=1)
        V = fice_mesh.get_periodic_space(params, mesh, dim=2)
    else:
        Qp = Q
        V = VectorFunctionSpace(mesh, 'Lagrange', 1, dim=2)

    data_mask = fice_mesh.get_mask(params, M)


    #Load fields
    U = Function(V,os.path.join(outdir,'U.xml'))
    alpha = Function(Qp,os.path.join(outdir,'alpha.xml'))
    beta = Function(Qp,os.path.join(outdir,'beta.xml'))

    bed = Function(Q,os.path.join(outdir, 'bed.xml'))
    bmelt = Function(M,os.path.join(outdir, 'bmelt.xml'))
    smb = Function(M,os.path.join(outdir, 'smb.xml'))
    thick = Function(M,os.path.join(outdir, 'thick.xml'))
    mask = Function(M,os.path.join(outdir, 'mask.xml'))
    mask_vel = Function(M,os.path.join(outdir, 'mask_vel.xml'))
    u_obs = Function(M,os.path.join(outdir, 'u_obs.xml'))
    v_obs = Function(M,os.path.join(outdir, 'v_obs.xml'))
    u_std = Function(M,os.path.join(outdir, 'u_std.xml'))
    v_std = Function(M,os.path.join(outdir, 'v_std.xml'))
    uv_obs = Function(M,os.path.join(outdir, 'uv_obs.xml'))

    #TODO - these solver params differ from run_inv.py
    # do we want to specify on a step-by-step basis?

    #Load Data
    # param = pickle.load( open( os.path.join(dd,'param.p'), "rb" ) )
    # param['sliding_law'] = sl

    # param['outdir'] = outdir
    # if sl == 0:
    #     param['picard_params'] =  {"nonlinear_solver":"newton",
    #                             "newton_solver":{"linear_solver":"umfpack",
    #                             "maximum_iterations":200,
    #                             "absolute_tolerance":1.0e-0,
    #                             "relative_tolerance":1.0e-3,
    #                             "convergence_criterion":"incremental",
    #                             "error_on_nonconvergence":False,
    #                             }}
    #     param['newton_params'] =  {"nonlinear_solver":"newton",
    #                             "newton_solver":{"linear_solver":"umfpack",
    #                             "maximum_iterations":25,
    #                             "absolute_tolerance":1.0e-7,
    #                             "relative_tolerance":1.0e-8,
    #                             "convergence_criterion":"incremental",
    #                             "error_on_nonconvergence":True,
    #                             }}

    # elif sl == 1:
    #     param['picard_params'] =  {"nonlinear_solver":"newton",
    #                             "newton_solver":{"linear_solver":"umfpack",
    #                             "maximum_iterations":200,
    #                             "absolute_tolerance":1.0e-4,
    #                             "relative_tolerance":1.0e-10,
    #                             "convergence_criterion":"incremental",
    #                             "error_on_nonconvergence":False,
    #                             }}
    #     param['newton_params'] =  {"nonlinear_solver":"newton",
    #                             "newton_solver":{"linear_solver":"umfpack",
    #                             "maximum_iterations":25,
    #                             "absolute_tolerance":1.0e-4,
    #                             "relative_tolerance":1.0e-5,
    #                             "convergence_criterion":"incremental",
    #                             "error_on_nonconvergence":True,
    #                             }}


    # param['n_steps'] = n_steps
    # param['num_sens'] = num_sens

    mdl = model.model(mesh, data_mask, params)
    mdl.init_bed(bed)
    mdl.init_thick(thick)
    mdl.gen_surf()
    mdl.init_mask(mask)
    mdl.init_vel_obs(u_obs,v_obs,mask_vel,u_std,v_std)
    mdl.init_lat_dirichletbc()
    mdl.init_bmelt(bmelt)
    mdl.init_smb(smb)
    mdl.init_alpha(alpha)
    mdl.init_beta(beta) #TODO <- should this be perturbed? likewise in other run_*.py
    mdl.label_domain()

    #Solve
    slvr = solver.ssa_solver(mdl)
    slvr.save_ts_zero()

    cntrl = slvr.get_control()[0] #TODO - generalise

    qoi_func =  slvr.get_qoi_func()

    #TODO here - cntrl now returns a list - so compute_gradient returns a list of tuples

    #Run the forward model
    Q = slvr.timestep(adjoint_flag=1, qoi_func=qoi_func)
    #Run the adjoint model, computing gradient of Qoi w.r.t cntrl
    dQ_ts = compute_gradient(Q, cntrl) #Isaac 27

    #Uncomment for Taylor Verification, Comment above two lines
    # param['num_sens'] = 1
    # J = slvr.timestep(adjoint_flag=1, cst_func=slvr.comp_Q_vaf)
    # dJ = compute_gradient(J, slvr.alpha)
    #
    #
    # def forward_ts(alpha_val=None):
    #     slvr.reset_ts_zero()
    #     if alpha_val:
    #         slvr.alpha = alpha_val
    #     return slvr.timestep(adjoint_flag=1, cst_func=slvr.comp_Q_vaf)
    #
    #
    # min_order = taylor_test(lambda alpha : forward_ts(alpha_val = alpha), slvr.alpha,
    #   J_val = J.value(), dJ = dJ, seed = 1e-2, size = 6)
    # sys.exit(os.EX_OK)

    #Output model variables in ParaView+Fenics friendly format
    outdir = params.io.output_dir

    #File(os.path.join(outdir,'mesh_test.xml')) << mdl.mesh

    #Output QOI & DQOI
    inout.write_qval(slvr.Qval_ts, params)
    inout.write_dqval(dQ_ts, params)

    vtkfile = File(os.path.join(outdir,'U.pvd'))
    xmlfile = File(os.path.join(outdir,'U.xml'))
    vtkfile << slvr.U
    xmlfile << slvr.U

    vtkfile = File(os.path.join(outdir,'beta.pvd'))
    xmlfile = File(os.path.join(outdir,'beta.xml'))
    vtkfile << slvr.beta
    xmlfile << slvr.beta

    vtkfile = File(os.path.join(outdir,'bed.pvd'))
    xmlfile = File(os.path.join(outdir,'bed.xml'))
    vtkfile << mdl.bed
    xmlfile << mdl.bed

    vtkfile = File(os.path.join(outdir,'thick.pvd'))
    xmlfile = File(os.path.join(outdir,'thick.xml'))
    H = project(mdl.H, mdl.M)
    vtkfile << H
    xmlfile << H

    vtkfile = File(os.path.join(outdir,'mask.pvd'))
    xmlfile = File(os.path.join(outdir,'mask.xml'))
    vtkfile << mdl.mask
    xmlfile << mdl.mask

    vtkfile = File(os.path.join(outdir,'mask_vel.pvd'))
    xmlfile = File(os.path.join(outdir,'mask_vel.xml'))
    vtkfile << mdl.mask_vel
    xmlfile << mdl.mask_vel

    vtkfile = File(os.path.join(outdir,'u_obs.pvd'))
    xmlfile = File(os.path.join(outdir,'u_obs.xml'))
    vtkfile << mdl.u_obs
    xmlfile << mdl.u_obs

    vtkfile = File(os.path.join(outdir,'v_obs.pvd'))
    xmlfile = File(os.path.join(outdir,'v_obs.xml'))
    vtkfile << mdl.v_obs
    xmlfile << mdl.v_obs

    vtkfile = File(os.path.join(outdir,'u_std.pvd'))
    xmlfile = File(os.path.join(outdir,'u_std.xml'))
    vtkfile << mdl.u_std
    xmlfile << mdl.u_std

    vtkfile = File(os.path.join(outdir,'v_std.pvd'))
    xmlfile = File(os.path.join(outdir,'v_std.xml'))
    vtkfile << mdl.v_std
    xmlfile << mdl.v_std

    vtkfile = File(os.path.join(outdir,'uv_obs.pvd'))
    xmlfile = File(os.path.join(outdir,'uv_obs.xml'))
    U_obs = project((mdl.v_obs**2 + mdl.u_obs**2)**(1.0/2.0), mdl.M)
    vtkfile << U_obs
    xmlfile << U_obs

    vtkfile = File(os.path.join(outdir,'alpha.pvd'))
    xmlfile = File(os.path.join(outdir,'alpha.xml'))
    vtkfile << slvr.alpha
    xmlfile << slvr.alpha


    vtkfile = File(os.path.join(outdir,'surf.pvd'))
    xmlfile = File(os.path.join(outdir,'surf.xml'))
    vtkfile << mdl.surf
    xmlfile << mdl.surf


if __name__ == "__main__":
    stop_annotating()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-t', '--time', dest='run_length', type=float, required=True, help='Number of years to run for')
    # parser.add_argument('-n', '--num_timesteps', dest='n_steps', type=int, required=True, help='Number of timesteps')
    # parser.add_argument('-s', '--num_sens', dest='num_sens', type=int, help='Number of samples of cost function')
    # parser.add_argument('-i', '--quantity_of_interest', dest='qoi', type=float,  help = 'Quantity of interest (0: VAF (default), 1: H^2 (for ISMIPC))')

    # parser.set_defaults(periodic_bc = False, nx=False,ny=False, outdir=False, num_sens = 1.0, pflag=0,sl=0, qoi=0)
    # args = parser.parse_args()

    # n_steps = args.n_steps
    # run_length = args.run_length
    # num_sens = args.num_sens
    # qoi = args.qoi

    assert len(sys.argv) == 2, "Expected a configuration file (*.toml)"
    run_forward(sys.argv[1])
