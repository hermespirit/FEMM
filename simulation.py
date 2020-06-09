# todo: add a readme + problem description
# todo : check whats the values outside boundaries when range ist too big


from random import gauss

from helpers import *

# simulation parameters :
n = 1  # number of simulation

# magnets material parameters
bHc_mu = 927500  # typical coercivity # todo: add non linear material
bHc_variation_on = False  # if false, the standard deviation of the coercivity is null
bHc_sigma = 22500  # standard deviation of coercivity

# magnets size parameter
# typical size of the magnet are 15x15mm and are defined by function define_halbach_magnet_config
magnet_size_variation_on = False  # if false, the standard deviation of the magnets size is null
magnet_size_sigma = 0.3  # standard deviation of magnet size

# parameters of the data extraction
x_range = (50, 55)
y_range = (45, 60)
dx = 1  # step size in mm
dy = 1  # step size in mm
simulation_result = []

# data processing parameters :

# simulation :
femm.openfemm(1)  # create an instance of femm without GUI
print('initialisation of the simulations')

# problem initialisation

list_magnets_prop = define_halbach_magnet_config()

for k in range(0, n):
	print('simulation %i of %i' % ((k + 1), (n)))

	# problem definition
	femm.newdocument(0)  # TODO:python geometry def
	femm.mi_probdef(0, 'millimeters', 'planar', 1.e-8, 0, 30)
	femm.mi_saveas('temp.fem')

	# geometry definition
	for magnet_prop in list_magnets_prop:

		if magnet_size_variation_on:  # compute randomised bHc value if activated
			width_variation = gauss(0, magnet_size_sigma)
			length_variation = gauss(0, magnet_size_sigma)
		else:
			width_variation = 0
			length_variation = 0

		femm.mi_drawrectangle(magnet_prop["coordinates"][0] - (magnet_prop["size"][0] + width_variation) / 2,
							  magnet_prop["coordinates"][1] - (magnet_prop["size"][1] + length_variation) / 2,
							  magnet_prop["coordinates"][0] + (magnet_prop["size"][0] + width_variation) / 2,
							  magnet_prop["coordinates"][1] + (magnet_prop["size"][1] + length_variation) / 2)
		femm.mi_addblocklabel(magnet_prop["coordinates"][0], magnet_prop["coordinates"][1])

	# boundaries conditions
	femm.mi_makeABC()

	# airbox creation # TODO: add airbox coordinates as a program input
	femm.mi_addblocklabel(1, 1)  # air block (airbox) : the coordinates of the label must be outside of any magnet
	femm.mi_getmaterial('Air')
	femm.mi_selectlabel(1, 1)  # enter the coordinates of a point in the airbox
	femm.mi_setblockprop('Air', 0, 1, '<None>', 0, 0, 0)
	femm.mi_clearselected()

	# materials properties
	# todo: check mat prop
	# todo: add different nat options to choose from so the name is accurate

	for magnet_prop in list_magnets_prop:

		if bHc_variation_on:  # compute randomised bHc value if activated
			bHc_random = gauss(bHc_mu, bHc_sigma)
		else:
			bHc_random = bHc_mu

		femm.mi_addmaterial('N48_' + str(int(bHc_random)), 1.05, 1.05, bHc_random, 0, 0.667, 0, 0, 1, 0, 0, 0, 0,
							0)  # mi_addmaterial(’matname’, mu x, mu y, H c, J, Cduct, Lam d, Phi hmax, lam fill, LamType, Phi hx, Phi hy, nstr, dwire) # todo: improve naming so that two materials do not take the same name
		femm.mi_selectlabel(magnet_prop["coordinates"][0], magnet_prop["coordinates"][1])
		femm.mi_setblockprop('N48_' + str(int(bHc_random)), 1, 1, '<None>', magnet_prop["magdir"], 0,
							 0)  # setblockprop(’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns)
		femm.mi_clearselected()

	femm.mi_analyze()
	femm.mi_loadsolution()
	simulation_result.append(extract_magnetic_field_map(x_range, y_range, dx, dy))

print('end of the simulations')
femm.closefemm()  # close the instance of femm

# data processing
