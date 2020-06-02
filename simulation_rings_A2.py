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

import femm
import matplotlib.pyplot as plt
import numpy

femm.openfemm(1)  # create an instance of femm without GUI, enter 0 instead of 1 to activate the GUI

# problem definition
femm.newdocument(0)  # create new magnetic problem preprocessor document

femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0,
                30)  # Define the problem type. Magnetostatic; Units of mm; Axisymmetric; Precision of 10^(-8) for the linear solver; a placeholder of 0 for the depth dimension, and an angle constraint of 30 degrees

# materials properties
femm.mi_getmaterial('Air')  # fetches the material called air from the materials library
femm.mi_getmaterial('N48')


# magnet creation

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


add_ring_magnet(2.5, 2, 2, 6, 'N48', 90)  # inner ring
add_ring_magnet(2.5, 5, 6, 15, 'N48', 270)  # outer ring

# boundaries conditions
femm.mi_makeABC()  # simulate an open boundary condition

# airbox creation
femm.mi_addblocklabel(1, 1)  # air block (airbox) : the coordinates of the label must be outside of any magnet

femm.mi_selectlabel(1, 1)  # assign the material to the airbox
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0)
femm.mi_clearselected()

femm.mi_zoomnatural()  # to check geometry while debugging
femm.mi_saveas('A2_concentric_rings.fem')

# meshing
# automatically done by the analysis function

# analysis
femm.mi_analyze()

# result data export
femm.mi_loadsolution()

# plot the flux density along z axis
zee = []
bee = []
for n in range(-0, 30):
    b = femm.mo_getb(0, n)
    zee.append(n)
    bee.append(b[1])

plt.plot(zee, bee)
plt.ylabel('Flux Density, Tesla')
plt.xlabel('Distance along the z-axis, mm')
plt.title('Plot of flux density along the axis')
plt.grid()
plt.show()

# export 2D data in csv file with numpy

B_data_2D = numpy.array([])

for r in range(0, 20):  # radial data range
    zee = []
    bee = []
    for z in range(-10, 10):  # axial data range
        b = femm.mo_getb(r, z)
        # zee.append(z)
        bee.append(b[1])
    B_data_2D = numpy.append(B_data_2D, bee, axis=0)

numpy.savetxt('B_A2_20x20mm.data', B_data_2D, delimiter=',')

femm.closefemm()  # close the instance of femm
