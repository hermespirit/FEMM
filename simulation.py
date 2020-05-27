import femm

femm.openfemm()  # create an instance of femm without GUI

# problem definition
femm.newdocument(0)  # create new magnetic problem preprocessor document

# geometry definition

# boundaries conditions

# materials properties

# meshing

# analysis

# result data export

femm.closefemm()  # close the instance of femm
