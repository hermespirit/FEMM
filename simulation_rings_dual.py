# This program is inspired of pyfemm example demo2, although slightly simpler.
# The problem consider an axisymmetric magnetostatic problem
# of two concentric 'N48' neodymium ring magnets (called Assembly 2 or A2).
# The centers of both rings are overlapped, but the rings have reverse magnetization directions.
# The outer ring has a height of 5mm, an inner radius of 6 mm, and an outer radius of 15 mm.
# The inner ring has a height of 2mm, an inner radius of 2 mm, and an outer radius of 6 mm.
# The objective of the analysis is to
# determine the flux density at the center of the ring magnet,
# and to plot the field along the r=0 axis. This analysis
# uses Femm materials library for material properties and employs an
# asymptotic boundary condition to approximate an "open"
# boundary condition on the edge of the solution domain.


from random import gauss

import numpy as np

from helpers import *

# simulation parameters :
n = 3  # number of simulation

# magnets material parameters
bHc_mu = 907500  # typical coercivity (kA/m) # todo: add non linear material
bHc_variation_on = False  # if false, the standard deviation of the coercivity is null
bHc_sigma = 15833  # standard deviation of coercivity

# magnets size parameter
# typical size of the magnet are 15x15mm and are defined by function define_halbach_magnet_config
magnet_size_variation_on = False  # if false, the standard deviation of the magnets size is null
magnet_size_sigma = 0.03  # standard deviation of magnet size

# magnets position parameter
# position of the magnets are define in define_halbach_magnet_config
magnet_position_variation_on = False  # if false, the standard deviation of the magnets position is null
magnet_position_sigma = 0.03  # standard deviation of magnet position
dual_magnet_distance = np.linspace(15.24, 25.4, n)

# parameters of the data extraction
x_range = (0, 0)
y_range = (12.7, 12.7 + 26)
dx = 1  # step size in mm
dy = 0.1  # step size in mm
simulation_result = []

# data processing parameters :
subject_area_size = (1, 1)  # size of the square on which the homogeneity is calculated

# simulation :
femm.openfemm(0)  # create an instance of femm without GUI
print('initialisation of the simulations')


def draw_ring_magnet(center_coordinate_z, height, inner_radius, outer_radius):
    # draw rectangle
    femm.mi_drawrectangle(inner_radius, center_coordinate_z - (height / 2), outer_radius,
                          center_coordinate_z + (height / 2))
    pass


def add_ring_magnet(center_coordinate_z, height, inner_radius, outer_radius, material, magnetization_direction):
    # draw rectangle
    draw_ring_magnet(center_coordinate_z, height, inner_radius, outer_radius)
    # add block label
    femm.mi_addblocklabel((inner_radius + outer_radius) / 2, center_coordinate_z)
    femm.mi_selectlabel((inner_radius + outer_radius) / 2,
                        center_coordinate_z)  # assign the material to the outer block
    femm.mi_setblockprop(material, 0, 1, '<None>', magnetization_direction, 0,
                         0)  # setblockprop(’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns)
    femm.mi_clearselected()

    # return label coordinate
    return ((inner_radius + outer_radius) / 2, center_coordinate_z)


# problem initialisation

list_magnets_prop = define_ring_magnet_config()  # 'x12magnets' to change config
k = 0  # number of simulation succeeded
while k < n:
    print('simulation %i of %i' % ((k + 1), (n)))

    # problem definition
    femm.newdocument(0)  # TODO:python geometry def
    femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0, 30)
    femm.mi_saveas('temp.fem')

    # magnet definition
    for magnet_prop in list_magnets_prop:

        if magnet_size_variation_on:  # compute randomised bHc value if activated
            width_variation = gauss(0, magnet_size_sigma)
            length_variation = gauss(0, magnet_size_sigma)
        else:
            width_variation = 0
            length_variation = 0

        if magnet_position_variation_on:  # compute randomised bHc value if activated
            abscissa_variation = gauss(0, magnet_position_sigma)
            ordinate_variation = gauss(0, magnet_position_sigma)
        else:
            abscissa_variation = 0
            ordinate_variation = 0
        if magnet_prop["name"] == 'upper_ring':
            center = magnet_prop["center_coordinate_z"] + dual_magnet_distance[k]
        else:
            center = magnet_prop["center_coordinate_z"]
        print(center)

        if bHc_variation_on:  # compute randomised bHc value if activated
            bHc_random = gauss(bHc_mu, bHc_sigma)
        else:
            bHc_random = bHc_mu

        # create material
        femm.mi_addmaterial('N48_' + str(int(bHc_random)), 1.05, 1.05, bHc_random, 0, 0.667, 0, 0, 1, 0, 0, 0, 0,
                            0)  # mi_addmaterial(’matname’, mu x, mu y, H c, J, Cduct, Lam d, Phi hmax, lam fill, LamType, Phi hx, Phi hy, nstr, dwire) # todo: improve naming so that two materials do not take the same name

        add_ring_magnet(center, magnet_prop["height"], magnet_prop["inner_radius"], magnet_prop["outer_radius"],
                        'N48_' + str(int(bHc_random)), magnet_prop["magnetization_direction"])

    # boundaries conditions
    femm.mi_makeABC()

    # airbox creation # TODO: add airbox coordinates as a program input
    femm.mi_addblocklabel(1, 1)  # air block (airbox) : the coordinates of the label must be outside of any magnet
    femm.mi_getmaterial('Air')
    femm.mi_selectlabel(1, 1)  # enter the coordinates of a point in the airbox
    femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0)
    femm.mi_clearselected()

    try:
        femm.mi_analyze()
        femm.mi_loadsolution()
        simulation_result.append(extract_magnetic_field_map(x_range, y_range, dx, dy))
        print('simulation succeeded')
        k += 1

    except:
        print("simulation failed")

print('end of the simulations')
femm.closefemm()  # close the instance of femm

x_axis = np.linspace(0, 26, simulation_result[0].size)
for result in simulation_result:
    plt.plot(x_axis, result[0])
plt.grid()
plt.xlabel('Distance along z axis (mm)')
plt.ylabel('B0z (T)')
plt.title('Dual magnet (h/IR/OR:6/12.7/25.4 mm) with varying distance')
plt.legend(('15.24 mm', '20.32 mm', '25.40 mm'))
plt.show()
