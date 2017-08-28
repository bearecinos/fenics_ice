import sys
from fenics import *
sys.path.insert(0,'../code/')
import model
import solver
import matplotlib.pyplot as plt
from IPython import embed

#Load Data

dd = '../input/grnld_tst/'
data_mesh = Mesh(''.join([dd,'grnld_mesh.xml']))
Q = FunctionSpace(data_mesh, 'Lagrange', 1)
bed = Function(Q,''.join([dd,'grnld_mesh_bed.xml']))
surf = Function(Q,''.join([dd,'grnld_mesh_surf.xml']))
bmelt = Function(Q,''.join([dd,'grnld_mesh_bmelt.xml']))
bdrag = Function(Q,''.join([dd,'grnld_mesh_bdrag.xml']))

#Generate model mesh
nx = 150
ny = 150
mesh = RectangleMesh(Point(0,0), Point(150e3, 150e3), nx, ny)


#Initialize Model
mdl = model.model(mesh)
mdl.init_surf(surf)
mdl.init_bed(bed)
mdl.init_thick()
mdl.init_bmelt(bmelt)
mdl.init_bdrag(bdrag)
mdl.default_solver_params()

mdl.gen_ice_mask()
mdl.gen_boundaries()

#Solve
slvr = solver.ssa_solver(mdl)

vtkfile = File('U.pvd')
U = project(mdl.U*365*24*3600,mdl.V)
vtkfile << U

vtkfile = File('bed.pvd')
vtkfile << mdl.bed

vtkfile = File('surf.pvd')
vtkfile << mdl.surf

vtkfile = File('thick.pvd')
vtkfile << mdl.thick

vtkfile = File('mask.pvd')
vtkfile << mdl.mask
