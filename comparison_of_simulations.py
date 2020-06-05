import femm
import matplotlib.pyplot as plt
import numpy

GUI_on = False  # to display colormap of each simulation

# files of the simulations to be compared
file_name_1 = 'file1.FEM'
file_name_2 = 'file2.FEM'

# parameters of the data extraction
x_range = (45, 60)
y_range = (45, 60)
dx = 0.1  # step size in mm
dy = 0.1  # step size in mm


def extract_magnetic_field_map(range_a, range_o, delta_abscissa, delta_ordinate):
    # todo: calculate the norm of b instead of transversal fetching
    # extract the transversal component of the magnetic flux of the solution loaded in femm (last '.ans' file created)
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


def simulation_from_fem_file(file_name, GUI):  # todo should it take range values and extraction paramters ?
    # run the simulation of the given file and extract the data
    # if the GUI is true, the data is also displayed as a colormap with matplotlib
    femm.opendocument(file_name)

    femm.mi_saveas('temp.FEM')

    femm.mi_analyze()

    # result data export
    femm.mi_loadsolution()

    # export 2D data in csv file with numpy
    B_map = extract_magnetic_field_map(x_range, y_range, dx, dy)

    if GUI:
        plt.imshow(B_map)
        plt.show()
    return B_map


# simulation
femm.openfemm(1)

Bmap1 = simulation_from_fem_file(file_name_1, GUI_on)
Bmap2 = simulation_from_fem_file(file_name_2, GUI_on)

femm.closefemm()  # close the instance of femm

# data processing

diff = Bmap2 - Bmap1
numpy.savetxt('comparison.data', diff, delimiter=',')
