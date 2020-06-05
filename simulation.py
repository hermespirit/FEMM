# todo: add a readme + problem description
# todo : check whats the values outside boundaries when range ist too big


from random import gauss

import femm

from comparison_of_simulations import extract_magnetic_field_map

# simulation parameters :
n = 2  # number of simulation

# material parameters
bHc_mu = 927.5  # typical coercivity # todo: add non linear material
bHc_variation_on = True  # if false, the standard deviation of the coercivity is null
bHc_sigma = 22.5  # standard deviation of coercivity

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
femm.opendocument('P3_N48_size2.FEM')  # TODO:python geometry def
femm.mi_saveas('temp.fem')

list_magnets_prop = []
list_magnets_prop.append({"coordinates": (52.5, 75), "magdir": 90})
list_magnets_prop.append({"coordinates": (52.5, 25), "magdir": 90})
list_magnets_prop.append({"coordinates": (34, 69), "magdir": 180})
list_magnets_prop.append({"coordinates": (68, 68), "magdir": 0})
list_magnets_prop.append({"coordinates": (75, 52), "magdir": 270})
list_magnets_prop.append({"coordinates": (69, 34), "magdir": 180})
list_magnets_prop.append({"coordinates": (37, 35), "magdir": 360})
list_magnets_prop.append({"coordinates": (30, 55), "magdir": 270})

for k in range(0, n):
	print('simulation %i of %i' % ((k + 1), (n)))

	# problem definition

	# geometry definition

	# boundaries conditions

	# materials properties
	# todo: check mat prop
	# todo: add different nat options to choose from so the name is accurate

	for magnet_prop in list_magnets_prop:

		if bHc_variation_on:  # compute randomised bHc value if activated
			bHc_random = gauss(bHc_mu, bHc_sigma)
		else:
			bHc_random = bHc_mu

		femm.mi_addmaterial('N48_' + str(int(1000 * bHc_random)), 1.05, 1.05, bHc_random, 0, 0.667, 0, 0, 1, 0, 0, 0, 0,
							0)  # mi_addmaterial(’matname’, mu x, mu y, H c, J, Cduct, Lam d, Phi hmax, lam fill, LamType, Phi hx, Phi hy, nstr, dwire) # todo: improve naming so that two materials do not take the same name
		femm.mi_selectlabel(magnet_prop["coordinates"][0], magnet_prop["coordinates"][1])
		femm.mi_setblockprop('N48_' + str(int(1000 * bHc_random)), 1, 1, '<None>', magnet_prop["magdir"], 0,
							 0)  # setblockprop(’blockname’, automesh, meshsize, ’incircuit’, magdir, group, turns)
		femm.mi_clearselected()

	femm.mi_analyze()
	femm.mi_loadsolution()
	simulation_result.append(extract_magnetic_field_map(x_range, y_range, dx, dy))

print('end of the simulations')
femm.closefemm()  # close the instance of femm

# data processing
