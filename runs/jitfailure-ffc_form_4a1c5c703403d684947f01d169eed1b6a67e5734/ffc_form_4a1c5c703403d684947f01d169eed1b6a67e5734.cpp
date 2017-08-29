// This code conforms with the UFC specification version 2017.1.0
// and was automatically generated by FFC version 2017.1.0.
// 
// This code was generated with the following parameters:
// 
//   add_tabulate_tensor_timing:     False
//   convert_exceptions_to_warnings: False
//   cpp_optimize:                   True
//   cpp_optimize_flags:             '-O2'
//   epsilon:                        1e-14
//   error_control:                  False
//   form_postfix:                   False
//   format:                         'ufc'
//   generate_dummy_tabulate_tensor: False
//   max_signature_length:           0
//   no-evaluate_basis_derivatives:  True
//   optimize:                       True
//   precision:                      None
//   quadrature_degree:              None
//   quadrature_rule:                None
//   representation:                 'auto'
//   split:                          False

#include "ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734.h"

// Based on https://gcc.gnu.org/wiki/Visibility
#if defined _WIN32 || defined __CYGWIN__
    #ifdef __GNUC__
        #define DLL_EXPORT __attribute__ ((dllexport))
    #else
        #define DLL_EXPORT __declspec(dllexport)
    #endif
#else
    #define DLL_EXPORT __attribute__ ((visibility ("default")))
#endif

ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise::ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise() : ufc::cell_integral()
{

}

ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise::~ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise()
{

}

const std::vector<bool> & ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise::enabled_coefficients() const
{
static const std::vector<bool> enabled({true});
return enabled;
}

void ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise::tabulate_tensor(double * A,
                                    const double * const * w,
                                    const double * coordinate_dofs,
                                    int cell_orientation) const
{
    // This function was generated using 'uflacs' representation
    // with the following integrals metadata:
    // 
    //   num_cells:         None
    //   optimize:          True
    //   precision:         16
    //   quadrature_degree: 4
    //   quadrature_rule:   'default'
    //   representation:    'uflacs'
    // 
    // and the following integral 0 metadata:
    // 
    //   estimated_polynomial_degree: 4
    //   optimize:                    True
    //   precision:                   16
    //   quadrature_degree:           4
    //   quadrature_rule:             'default'
    //   representation:              'uflacs'
    
    // Quadrature rules
    alignas(32) static const double weights6[6] = { 0.054975871827661, 0.054975871827661, 0.054975871827661, 0.1116907948390055, 0.1116907948390055, 0.1116907948390055 };
    // Precomputed values of basis functions and precomputations
    // FE* dimensions: [entities][points][dofs]
    // PI* dimensions: [entities][dofs][dofs] or [entities][dofs]
    // PM* dimensions: [entities][dofs][dofs]
    alignas(32) static const double FE3_C0_D01_Q6[1][1][2] = { { { -1.0, 1.0 } } };
    alignas(32) static const double FE6_C0_Q6[1][6][6] =
        { { { -0.07480380774819596, 0.5176323419876736, -0.07480380774819667, 0.299215230992787, 0.03354481152314823, 0.2992152309927838 },
            { -0.07480380774819598, -0.07480380774819669, 0.5176323419876736, 0.2992152309927871, 0.2992152309927837, 0.03354481152314844 },
            { 0.5176323419876714, -0.07480380774819669, -0.07480380774819667, 0.03354481152314868, 0.2992152309927866, 0.2992152309927866 },
            { -0.04820837781551194, -0.08473049309397786, -0.04820837781551193, 0.1928335112620479, 0.7954802262009059, 0.1928335112620479 },
            { -0.04820837781551193, -0.04820837781551195, -0.08473049309397784, 0.1928335112620479, 0.1928335112620478, 0.7954802262009062 },
            { -0.08473049309397775, -0.04820837781551199, -0.04820837781551193, 0.795480226200906, 0.1928335112620478, 0.1928335112620479 } } };
    // Unstructured piecewise computations
    const double J_c0 = coordinate_dofs[0] * FE3_C0_D01_Q6[0][0][0] + coordinate_dofs[2] * FE3_C0_D01_Q6[0][0][1];
    const double J_c3 = coordinate_dofs[1] * FE3_C0_D01_Q6[0][0][0] + coordinate_dofs[5] * FE3_C0_D01_Q6[0][0][1];
    const double J_c1 = coordinate_dofs[0] * FE3_C0_D01_Q6[0][0][0] + coordinate_dofs[4] * FE3_C0_D01_Q6[0][0][1];
    const double J_c2 = coordinate_dofs[1] * FE3_C0_D01_Q6[0][0][0] + coordinate_dofs[3] * FE3_C0_D01_Q6[0][0][1];
    alignas(32) double sp[4];
    sp[0] = J_c0 * J_c3;
    sp[1] = J_c1 * J_c2;
    sp[2] = sp[0] + -1 * sp[1];
    sp[3] = std::abs(sp[2]);
    alignas(32) double BF0[6] = {};
    for (int iq = 0; iq < 6; ++iq)
    {
        // Quadrature loop body setup (num_points=6)
        // Unstructured varying computations for num_points=6
        double w0 = 0.0;
        for (int ic = 0; ic < 6; ++ic)
            w0 += w[0][ic] * FE6_C0_Q6[0][iq][ic];
        alignas(32) double sv6[1];
        sv6[0] = sp[3] * std::max(w0, 10);
        const double fw0 = sv6[0] * weights6[iq];
        for (int i = 0; i < 6; ++i)
            BF0[i] += fw0 * FE6_C0_Q6[0][iq][i];
    }
    std::fill(&A[0], &A[6], 0.0);
    for (int i = 0; i < 6; ++i)
        A[i] += BF0[i];
}

extern "C" DLL_EXPORT ufc::cell_integral * create_ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise()
{
  return new ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise();
}


ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main() : ufc::form()
{
    // Do nothing
}

ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::~ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main()
{
    // Do nothing
}

const char * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::signature() const
{
    return "3a3faa55b4f986224d648fb8bab8ad87b2531fcf5ba64304eeda8fedc278d7d6830f72d8fc0d835c6b58aa6d6a28c8ed33647b635221c192dab8950521e8b475";
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::rank() const
{
    return 1;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::num_coefficients() const
{
    return 1;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::original_coefficient_position(std::size_t i) const
{
    static const std::vector<std::size_t> position({0});
    return position[i];
}

ufc::finite_element * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_coordinate_finite_element() const
{
    return create_ffc_element_e4ca4e1f53ebcead7e6b02aa6dd6b9681bebaa84_finite_element_main();
}

ufc::dofmap * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_coordinate_dofmap() const
{
    return create_ffc_element_e4ca4e1f53ebcead7e6b02aa6dd6b9681bebaa84_dofmap_main();
}

ufc::coordinate_mapping * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_coordinate_mapping() const
{
    return nullptr;
}

ufc::finite_element * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_finite_element(std::size_t i) const
{
    switch (i)
    {
    case 0:
      {
        return create_ffc_element_b59901cca386b6bb04a11bab2946c683329d8a30_finite_element_main();
        break;
      }
    case 1:
      {
        return create_ffc_element_b59901cca386b6bb04a11bab2946c683329d8a30_finite_element_main();
        break;
      }
    }
    
    return 0;
}

ufc::dofmap * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_dofmap(std::size_t i) const
{
    switch (i)
    {
    case 0:
      {
        return create_ffc_element_b59901cca386b6bb04a11bab2946c683329d8a30_dofmap_main();
        break;
      }
    case 1:
      {
        return create_ffc_element_b59901cca386b6bb04a11bab2946c683329d8a30_dofmap_main();
        break;
      }
    }
    
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_cell_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_exterior_facet_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_interior_facet_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_vertex_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_custom_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_cutcell_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_interface_subdomain_id() const
{
    return 0;
}

std::size_t ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::max_overlap_subdomain_id() const
{
    return 0;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_cell_integrals() const
{
    return true;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_exterior_facet_integrals() const
{
    return false;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_interior_facet_integrals() const
{
    return false;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_vertex_integrals() const
{
    return false;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_custom_integrals() const
{
    return false;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_cutcell_integrals() const
{
    return false;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_interface_integrals() const
{
    return false;
}

bool ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::has_overlap_integrals() const
{
    return false;
}

ufc::cell_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_cell_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::exterior_facet_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_exterior_facet_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::interior_facet_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_interior_facet_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::vertex_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_vertex_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::custom_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_custom_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::cutcell_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_cutcell_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::interface_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_interface_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::overlap_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_overlap_integral(std::size_t subdomain_id) const
{
    return 0;
}

ufc::cell_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_cell_integral() const
{
    return new ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_cell_integral_main_otherwise();
}

ufc::exterior_facet_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_exterior_facet_integral() const
{
    return 0;
}

ufc::interior_facet_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_interior_facet_integral() const
{
    return 0;
}

ufc::vertex_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_vertex_integral() const
{
    return 0;
}

ufc::custom_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_custom_integral() const
{
    return 0;
}

ufc::cutcell_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_cutcell_integral() const
{
    return 0;
}

ufc::interface_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_interface_integral() const
{
    return 0;
}

ufc::overlap_integral * ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main::create_default_overlap_integral() const
{
    return 0;
}

extern "C" DLL_EXPORT ufc::form * create_ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main()
{
  return new ffc_form_4a1c5c703403d684947f01d169eed1b6a67e5734_form_main();
}

