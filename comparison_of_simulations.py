import femm
import matplotlib.pyplot as plt
import numpy

from helpers import extract_magnetic_field_map

GUI_on = True  # to display colormap of each simulation

# files of the simulations to be compared
file_name_1 = 'file1.FEM'
file_name_2 = 'file2.FEM'

# parameters of the data extraction
x_range = (45 - 52.5, 60 - 52.5)
y_range = (45 - 52.5, 60 - 52.5)
dx = 0.1  # step size in mm
dy = 0.1  # step size in mm


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
# x_range = (45, 60)
# y_range = (45, 60)
Bmap2 = simulation_from_fem_file(file_name_2, GUI_on)

femm.closefemm()  # close the instance of femm

# data processing

diff = Bmap2 - Bmap1
numpy.savetxt('comparison.data', diff, delimiter=',')
