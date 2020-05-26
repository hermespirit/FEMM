# This program is inspired of pyfemm exemple demo2, although a lot simpler.
# The problem consider an axisymmetric magnetostatic problem
# of a 'N48' neodymium ring magnet with a height of 5mm, an
# inner radius of 6 mm, and an outer radius of 15 mm. The objective of the analysis is to
# determine the flux density at the center of the ring magnet,
# and to plot the field along the r=0 axis. This analysis
# uses Femm materials library for material properties and employs an
# asymptotic boundary condition to approximate an "open"
# boundary condition on the edge of the solution domain.

import femm
import matplotlib.pyplot as plt

femm.openfemm()  # create an instance of femm without GUI

# problem definition
femm.newdocument(0)  # create new magnetic problem preprocessor document

femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0,
                30)  # Define the problem type. Magnetostatic; Units of mm; Axisymmetric; Precision of 10^(-8) for the linear solver; a placeholder of 0 for the depth dimension, and an angle constraint of 30 degrees

# geometry definition
femm.mi_drawrectangle(6, 0, 15, 5)  # draw a rectangle for the ring magnet;

# boundaries conditions
femm.mi_makeABC()  # simulate an open boundary condition

# materials properties
femm.mi_addblocklabel(1, 1)  # air block (airbox)
femm.mi_addblocklabel(10, 3)  # ring block (neodymium)

femm.mi_getmaterial('Air')  # fetches the material called air from the materials library
femm.mi_getmaterial('N48')

femm.mi_selectlabel(10, 3)  # assign the material to the block
femm.mi_setblockprop('N48', 0, 1, '<None>', 90, 0,
                     0)  # setblockprop(’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns)
femm.mi_clearselected()

femm.mi_selectlabel(1, 1)
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0)
femm.mi_clearselected()

femm.mi_zoomnatural()  # to check geometry while debuging
femm.mi_saveas('ring.fem')

# meshing
# automaticaly done by the analysis function

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

femm.closefemm()  # close the instance of femm
