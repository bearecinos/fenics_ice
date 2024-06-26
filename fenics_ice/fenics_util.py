# For fenics_ice copyright information see ACKNOWLEDGEMENTS in the fenics_ice
# root directory

# This file is part of fenics_ice.
#
# fenics_ice is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# fenics_ice is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with tlm_adjoint.  If not, see <https://www.gnu.org/licenses/>.

from .backend import Constant, File, Function, FunctionSpace, Mesh, \
    VectorFunctionSpace, project

from . import model

import numpy as np
import sys
import os
from pylab import plt
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import collections.abc

def plot_variable(u, name, direc, cmap='gist_yarg', scale='lin', numLvls=12,
                  umin=None, umax=None, tp=False, tpAlpha=0.5, show=True,
                  hide_ax_tick_labels=False, label_axes=True, title='',
                  use_colorbar=True, hide_axis=False, colorbar_loc='right'):
  """
  """
  mesh = u.function_space().mesh()
  v    = u.compute_vertex_values(mesh)
  x    = mesh.coordinates()[:,0]
  y    = mesh.coordinates()[:,1]
  t    = mesh.cells()

  d    = os.path.dirname(direc)
  if not os.path.exists(d):
    os.makedirs(d)

  if umin != None:
    vmin = umin
  else:
    vmin = v.min()
  if umax != None:
    vmax = umax
  else:
    vmax = v.max()

  # countour levels :
  if scale == 'log':
    v[v < vmin] = vmin + 1e-12
    v[v > vmax] = vmax - 1e-12
    from matplotlib.ticker import LogFormatter
    levels      = np.logspace(np.log10(vmin), np.log10(vmax), numLvls)
    formatter   = LogFormatter(10, labelOnlyBase=False)
    norm        = colors.LogNorm()

  elif scale == 'lin':
    v[v < vmin] = vmin + 1e-12
    v[v > vmax] = vmax - 1e-12
    from matplotlib.ticker import ScalarFormatter
    levels    = np.linspace(vmin, vmax, numLvls)
    formatter = ScalarFormatter()
    norm      = None

  elif scale == 'bool':
    from matplotlib.ticker import ScalarFormatter
    levels    = [0, 1, 2]
    formatter = ScalarFormatter()
    norm      = None

  fig = plt.figure(figsize=(5,5))
  ax  = fig.add_subplot(111)

  c = ax.tricontourf(x, y, t, v, levels=levels, norm=norm,
                     cmap=plt.get_cmap(cmap))
  plt.axis('equal')

  if tp == True:
    p = ax.triplot(x, y, t, '-', lw=0.2, alpha=tpAlpha)
  ax.set_xlim([x.min(), x.max()])
  ax.set_ylim([y.min(), y.max()])
  if label_axes:
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$y$')
  if hide_ax_tick_labels:
    ax.set_xticklabels([])
    ax.set_yticklabels([])
  if hide_axis:
    plt.axis('off')

  # include colorbar :
  if scale != 'bool' and use_colorbar:
    divider = make_axes_locatable(plt.gca())
    cax  = divider.append_axes(colorbar_loc, "5%", pad="3%")
    cbar = plt.colorbar(c, cax=cax, format=formatter,
                        ticks=levels)
    tit = plt.title(title)

  if use_colorbar:
    plt.tight_layout(rect=[.03,.03,0.97,0.97])
  else:
    plt.tight_layout()
  plt.savefig(os.path.join(direc, name + '.png'), dpi=300)
  if show:
    plt.show()
  plt.close(fig)

def plot_inv_conv(fvals, name, direc):
    plt.figure()
    plt.semilogy(fvals, 'ko-')
    plt.xlabel('Iterations')
    plt.ylabel('Cost Function')
    plt.savefig(os.path.join(direc, name + '.png'), dpi=300)
    plt.close()


def binread(fn):
  fid = open(fn,"rb")
  file_contents = np.fromfile(fn, dtype='float64')
  if sys.byteorder == 'little': file_contents.byteswap(True)
  fid.close()
  return file_contents


def U2Uobs(dd,noise_sdev=1.0):
    """
    Takes a velocity field in 'U.xml' and adds normal noise
    Output written to 'u_obs.xml' and 'v_obs.xml'
    """

    data_mesh = Mesh(os.path.join(dd,'mesh.xml'))
    V = VectorFunctionSpace(data_mesh, 'Lagrange', 1, dim=2, constrained_domain=model.PeriodicBoundary(40e3))
    M = FunctionSpace(data_mesh, 'DG', 0)

    U = Function(V,os.path.join(dd,'U.xml'))
    N = Function(M)

    uu,vv = U.split(True)
    u = project(uu,M)
    v = project(vv,M)

    u_array = u.vector().array()
    v_array = v.vector().array()

    np.random.seed(0)
    u_noise = np.random.normal(scale=noise_sdev, size=u_array.size)
    v_noise = np.random.normal(scale=noise_sdev, size=v_array.size)

    u.vector().set_local(u.vector().array() + u_noise)
    v.vector().set_local(v.vector().array() + v_noise)

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



def dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def dict_clean_null_terms(d):
    """
    Strips dictionary items where value is None.
    Useful when specifying options to 3rd party lib
    where default should be 'missing' rather than None
    """
    return {
        k:v
        for k, v in d.items()
        if v is not None
    }

