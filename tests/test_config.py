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

import fenics_ice.backend as fe

import pytest
import numpy as np
import fenics_ice as fice
from fenics_ice import config, inout, test_domains
from pathlib import Path


###################
#     CONFIG      #
###################

@pytest.mark.short
def test_parse_config(temp_model):
    """Test the parsing of configuration files"""

    work_dir = temp_model["work_dir"]
    toml_file = temp_model["toml_filename"]

    assert (work_dir/toml_file).exists()

    params = config.ConfigParser(work_dir/toml_file, work_dir)

    assert params
    return params


###################
#     INOUT       #
###################

@pytest.mark.short
def test_git_info():
    """Test printing git branch"""
    inout.log_git_info()

@pytest.mark.short
def test_print_config(temp_model):
    """Testing printing out config"""
    params = test_parse_config(temp_model)
    inout.print_config(params)

@pytest.mark.short
def test_setup_logger(temp_model):
    """Test setting up the logger"""
    params = test_parse_config(temp_model)
    inout.setup_logging(params)

@pytest.mark.short
def test_input_data_read_and_interp(temp_model, monkeypatch):
    """Test the reading & interpolation of input data into InputData object"""

    work_dir = temp_model["work_dir"]
    toml_file = temp_model["toml_filename"]

    # Switch to the working directory
    monkeypatch.chdir(work_dir)

    params = test_parse_config(temp_model)
    dd = params.io.input_dir
    data_file = params.io.data_file

    # Load the mesh & input data
    inmesh = fice.mesh.get_mesh(params)
    indata = inout.InputData(params)

    # Create a function space for interpolation
    test_space = fe.FunctionSpace(inmesh, 'Lagrange', 1)

    # Check successfully reads bed & data_mask
    bed_interp = indata.interpolate("bed", test_space).vector()[:]

    # Check the actual value of an interpolated field:
    # TODO - this is a little ad hoc, can it be incorporated into test definition?
    if "ismip" in toml_file:
        # test_x = np.hsplit(test_space.tabulate_dof_coordinates(), 2)[0][:,0]
        test_y = np.hsplit(test_space.tabulate_dof_coordinates(), 2)[1][:, 0]
        test_bed = 1e4 - test_y*np.tan(0.1*np.pi/180.0) - 1e3

    elif "ice_stream" in toml_file:
        test_x = np.hsplit(test_space.tabulate_dof_coordinates(), 2)[0][:, 0]
        test_bed = -500.0 - (test_x / 500.0)
    else:
        raise Exception("Unrecognised test setup")

    assert np.linalg.norm(test_bed - bed_interp) < 1e-10

    # Check unfound data raises error...
    with pytest.raises(KeyError):
        indata.interpolate("a_madeup_name", test_space)

    # ...unless a default is supplied
    outfun = indata.interpolate("a_madeup_name", test_space, default=1.0)
    assert np.all(outfun.vector()[:] == 1.0)

    # Check that an out-of-bounds mesh returns an error
    bad_mesh = fe.UnitSquareMesh(2, 2)
    fe.MeshTransformation.translate(bad_mesh, fe.Point(-1e10, -1e10))
    bad_space = fe.FunctionSpace(bad_mesh, 'Lagrange', 1)
    with pytest.raises(ValueError):
        indata.interpolate("bed", bad_space)
