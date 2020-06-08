import femm
import numpy


def extract_magnetic_field_map(range_a, range_o, delta_abscissa, delta_ordinate):
    # todo: calculate the norm of b instead of transversal fetching
    # extract the transverse component of the magnetic flux of the solution loaded in femm (last '.ans' file created)
    # return the data as a 2D numpy array

    na = int((range_a[1] - range_a[0]) / delta_abscissa) + 1  # number of point on the abscissa axis
    no = int((range_o[1] - range_o[0]) / delta_ordinate) + 1  # number of point on the ordinate axis

    abscissa_axis = numpy.linspace(range_a[0], range_a[1], na)  # abscissa coordinates of data
    ordinate_axis = numpy.linspace(range_o[0], range_o[1], no)

    # coordinates_list = []
    b_list = []

    for j in abscissa_axis:
        for q in ordinate_axis:
            # coordinates_list.append((j, q))
            b_list.append(femm.mo_getb(j, q)[1])  # fetch the data in the femm solution for each data point

    b_map = numpy.asarray(b_list).reshape(na, no)
    return b_map


def define_halbach_magnet_config(config='0'):
    # todo: add return ?
    magnets_prop = []
    if config == 'x12magnets':
        magnets_prop.append({"coordinates": (0, 35), "magdir": 90, "size": (15, 15), "name": 'N_top'})
        magnets_prop.append({"coordinates": (0, 20), "magdir": 90, "size": (15, 15), "name": 'N_bottom'})

        magnets_prop.append({"coordinates": (17, 17), "magdir": 0, "size": (15, 15), "name": 'NE'})
        magnets_prop.append({"coordinates": (20, 0), "magdir": 270, "size": (15, 15), "name": 'E_left'})
        magnets_prop.append({"coordinates": (35, 0), "magdir": 270, "size": (15, 15), "name": 'E_right'})

        magnets_prop.append({"coordinates": (17, -17), "magdir": 180, "size": (15, 15), "name": 'SE'})
        magnets_prop.append({"coordinates": (0, -20), "magdir": 90, "size": (15, 15), "name": 'S_top'})
        magnets_prop.append({"coordinates": (0, -35), "magdir": 90, "size": (15, 15), "name": 'S_bottom'})

        magnets_prop.append({"coordinates": (-17, -17), "magdir": 0, "size": (15, 15), "name": 'SW'})
        magnets_prop.append({"coordinates": (-35, 0), "magdir": 270, "size": (15, 15), "name": 'W_left'})
        magnets_prop.append({"coordinates": (-20, 0), "magdir": 270, "size": (15, 15), "name": 'W_right'})

        magnets_prop.append({"coordinates": (-17, 17), "magdir": 180, "size": (15, 15), "name": 'NW'})
    else:
        magnets_prop = []
        magnets_prop.append({"coordinates": (0, 27.5), "magdir": 90, "size": (15, 30), "name": 'N'})
        magnets_prop.append({"coordinates": (17, 17), "magdir": 0, "size": (15, 15), "name": 'NE'})
        magnets_prop.append({"coordinates": (27.5, 0), "magdir": 270, "size": (30, 15), "name": 'E'})
        magnets_prop.append({"coordinates": (17, -17), "magdir": 180, "size": (15, 15), "name": 'SE'})
        magnets_prop.append({"coordinates": (0, -27.5), "magdir": 90, "size": (15, 30), "name": 'S'})
        magnets_prop.append({"coordinates": (-17, -17), "magdir": 0, "size": (15, 15), "name": 'SW'})
        magnets_prop.append({"coordinates": (-27.5, 0), "magdir": 270, "size": (30, 15), "name": 'W'})
        magnets_prop.append({"coordinates": (-17, 17), "magdir": 180, "size": (15, 15), "name": 'NW'})
    return magnets_prop
