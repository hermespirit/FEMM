# This program consider an axisymmetric magnetostatic problem
# of a cylindrical coil with an axial length of 100 mm, an
# inner radius of 50 mm, and an outer radius of 100 mm.  The
# coil has 200 turns and the coil current is 20 Amps. There is
# an iron bar 80 mm long with a radius of 10 mm centered co-
# axially with the coil.  The objective of the analysis is to
# determine the flux density at the center of the iron bar,
# and to plot the field along the r=0 axis. This analysis
# defines a nonlinear B-H curve for the iron and employs an
# asymptotic boundary condition to approximate an "open"
# boundary condition on the edge of the solution domain.

import femm
import matplotlib.pyplot as plt

# The package must be initialized with the openfemm command.
femm.openfemm();

# We need to create a new Magnetostatics document to work on.
femm.newdocument(0);

# Define the problem type.  Magnetostatic; Units of mm; Axisymmetric;
# Precision of 10^(-8) for the linear solver; a placeholder of 0 for
# the depth dimension, and an angle constraint of 30 degrees
femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0, 30);

# Draw a rectangle for the steel bar on the axis;
femm.mi_drawrectangle(0, -40, 10, 40);

# Define an "open" boundary condition using the built-in function:
femm.mi_makeABC()

# Add block labels, one to each the steel, coil, and air regions.
femm.mi_addblocklabel(5, 0);
femm.mi_addblocklabel(35, 15);

# Add some block labels materials properties
femm.mi_addmaterial('Air', 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0);
femm.mi_addmaterial('LinearIron', 2100, 2100, 0, 0, 0, 0, 0, 1, 0, 0, 0);

# Apply the materials to the appropriate block labels
femm.mi_selectlabel(5, 0);
femm.mi_setblockprop('LinearIron', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

femm.mi_selectlabel(35, 15);
femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0);
femm.mi_clearselected()

# Now, the finished input geometry can be displayed.
femm.mi_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.mi_saveas('coil.fem');

# Now,analyze the problem and load the solution when the analysis is finished
femm.mi_analyze()
femm.mi_loadsolution()

# If we were interested in the flux density at specific positions,
# we could inquire at specific points directly:
b0 = femm.mo_getb(0, 0);
print('Flux density at the center of the bar is %g T' % b0[1]);
b1 = femm.mo_getb(0, 50);
print('Flux density at r=0,z=50 is %g T' % b1[1]);

# Or we could, for example, plot the results along a line using
zee = []
bee = []
for n in range(-100, 101):
    b = femm.mo_getb(0, n);
    zee.append(n)
    bee.append(b[1]);

plt.plot(zee, bee)
plt.ylabel('Flux Density, Tesla')
plt.xlabel('Distance along the z-axis, mm')
plt.title('Plot of flux density along the axis')
plt.grid()
plt.show()

# When the analysis is completed, FEMM can be shut down.
femm.closefemm()
