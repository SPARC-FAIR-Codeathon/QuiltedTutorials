import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from stl import mesh as msh
from mpl_toolkits import mplot3d
from ipywidgets import interact, Checkbox, fixed, display

def get_position(percent, min_val, max_val):
    """ Converts the position from percentage to distance.

    Inputs:
    percent -- float, percentage value.
    min_val -- float, minimum distance for conversion.
    max_val -- float, maximum distance for conversion.

    Outputs:
    converted_value -- float, converted value.

    """
    return percent / 100 * (max_val - min_val) + min_val


def load_data(data_name, col_keeps, y_lims, z_lims):
    """ Loads the data from an .xlsx file.

    Inputs:
    data_name -- str, nane of the .xlsx file to read.
    col_keeps -- dict{str:str}, dictionnary containing the names of the columns
        to keep.
    y_lims -- list[int], limits for the y direction to convert back to mm,
            first element is the minimum and second is the maximum.
    z_lims -- list[int], limits for the z direction to convert back to mm,
        first element is the minimum and second is the maximum.

    Outputs:
    df -- DataFrame, data frame containing the desired data.

    """
    df = pd.read_excel(data_name)
    # remove unnecessary columns
    for col in df.columns:
        if col in col_keeps:
            df.rename(columns = {col:col_keeps[col]}, inplace = True)
        else:
            df.drop(col, axis=1, inplace=True)
    df['y'] = get_position(df['%y'], y_lims[0], y_lims[1])
    df['z'] = get_position(df['%x'], z_lims[0], z_lims[1]) # x becomes z
    df['-%y'] = 100 - df['%y']
    # change the area to mm
    return df


def convert_2D_data(df):
    data_array = np.array(df[['y','z','area']])

    # Convert input data to numpy coordinate array and intensity array.
    data_2_dim = np.array(data_array[:, (0,1)])
    data_intensity = data_array[:,2]

    return data_2_dim, data_intensity

def map_to_3D(input_pts, input_mesh):
    """ Maps an Nx2 numpy array of points in the y-z plane to have an
    x coordinate based on the nearest point in the y-z plane on the input mesh.

    Inputs:
    input_pts -- np.array(N, 2) with y coordinates in column 0, and
        z coordinates in column 1.
    input_mesh -- numpy-stl mesh object with the target mesh.

    Outputs:
    out: np.array(N, 3), numpy array with x coordinates in column 0,
        y coordinates in column 1, and z coordinates in column 2.

    """
    # Create list of vertices from the vectors of each triangle in the mesh.
    vert = np.around(np.unique(input_mesh.vectors.reshape(
        [int(input_mesh.vectors.size/3), 3]), axis=0),2)

    # select only vertices on the ventral stomach
    vert_ventral = vert[vert[:, 0] < 9.0, :]
    # initial output array
    out = np.zeros((input_pts.shape[0], 3))

    # iterate over all points in y-z plane and find the closest mesh vertex in this plane
    for i, pt in enumerate(input_pts):
        min_arg = np.argmin(np.sqrt(np.sum(np.power(
            np.abs((pt-vert_ventral[:, 1:3])),2), 1)))
        matched_x = vert_ventral[min_arg, 0]
        # Add some random movement so that triangles don't obscure points
        matched_x -= 2 - np.random.rand()*1
        out[i, :] = [matched_x, pt[0], pt[1]]
    return out

# Setup maximimum y and z widths based on scale in image.
z_lims = [0, 36.7]
y_lims = [4.6, 0]

col_keeps = {'%x (distance from pylorus side)':'%x', '%y (distance from bottom)':'%y',
             'Average IGLE Area (um²)':'area', 'Area Of Innervation':'area',
             'Neuron Area Of Innervation (um²) -Convex Hull':'area'}


df_igle = load_data('data/IGLE_data.xlsx', col_keeps, y_lims, z_lims)
df_ima = load_data('data/IMA_analyzed_data.xlsx', col_keeps, y_lims, z_lims)
df_efferent = load_data('data/Efferent_data.xlsx', col_keeps, y_lims, z_lims)

efferent_2D, efferent_intensity = convert_2D_data(df_efferent)
igle_2D, igle_intensity = convert_2D_data(df_igle)
ima_2D, ima_intensity = convert_2D_data(df_ima)

# Load the STL files and add the vectors to the plot
stomach_mesh = msh.Mesh.from_file('data/stom_surf_mesh.stl')

# with coordinate axes (imported with signs reversed)
stomach_mesh.x -= np.min(stomach_mesh.x.flatten())
stomach_mesh.y -= np.min(stomach_mesh.y.flatten())
stomach_mesh.z -= np.min(stomach_mesh.z.flatten())

# Project to 3D stomach surface.
efferent_3D = map_to_3D(efferent_2D, stomach_mesh)
igle_3D = map_to_3D(igle_2D, stomach_mesh)
ima_3D = map_to_3D(ima_2D, stomach_mesh)

# Enable interactivity in jupyterlab.
# %matplotlib widget

def plotting_fct(mesh, efferent_3D, igle_3D, ima_3D, efferent_intensity,
                 igle_intensity, ima_intensity, efferent, igle, ima):
    # Start a matplotlib 3d interactive figure.
    fig = plt.figure()
    fig.suptitle('Projection visualisation', fontsize=16)
    ax = fig.add_subplot(projection='3d')

    # Add mesh as triangle polygons to 3d matplotlib view.
    faces = mplot3d.art3d.Poly3DCollection(mesh.vectors, color=(0, 0.4470, 0.7410))
    faces.set_edgecolor((0, 0.4470, 0.7410, 0.1))
    faces.set_alpha(0.1)
    ax.add_collection3d(faces)

    # Plot the projected neurons coloured by their area of innervation.
    if efferent:
        ax.scatter(efferent_3D[:,0], efferent_3D[:,1], efferent_3D[:,2],
                   c=efferent_intensity, cmap='Greens')

    if ima:
        ax.scatter(ima_3D[:,0], ima_3D[:,1], ima_3D[:,2],
                   c=ima_intensity, cmap='Reds')

    if igle:
        ax.scatter(igle_3D[:,0], igle_3D[:,1], igle_3D[:,2],
                    c=igle_intensity, cmap='Blues')


    # Scale view to the mesh size and turn off axis chrome.
    ax.set_xlim(0,40)
    ax.set_ylim(-10,30)
    ax.set_zlim(-10,30)
    ax.axis('off')

    # Show ventral surface and plot projected neurons.
    ax.view_init(10, -57, 'y')
    plt.show()

