
import pandas as pd
from tqdm import tqdm
import requests
from zipfile import ZipFile
import os

from stl import mesh as msh
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
# from ipywidgets import interact, Checkbox, fixed, display

## Data search
## We are looking for interesting dataset

def search_dataset(query, limit=5):
    """ Searches the SPARC data portal for the given query
        Inputs: 
        query -- string to search as a keyword in the dataset
        limit -- integer limit for the number of results to return, defualt 5
        
        Outputs:
        rst -- string of concatenated json tags for return results with the id, version, name and tags fields only for all returned results
        
    """
    url = "https://api.pennsieve.io/discover/search/datasets?limit="+str(limit)+"&offset=0&query="+query+"&orderBy=relevance&orderDirection=desc"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    rst = []
    for r in response.json()['datasets']:
        rst += [{'id':r['id'], 'version':r['version'], 'name':r['name'], 'tags':r['tags']}]
    return rst

def print_folder_structure(dataId, version, max_level=3): # taken from stackoverflow
    """ Print the directory structure of a dataset to the console output. This assumes that it is saved in the root directory with default filename.
    
    Inputs: 
    dataId -- integer id of the result
    version -- integer dataset version 
    max_level -- integer depth of directory structure to return, default 3
    
    Outputs: 
    None 
    """
    startpath = "Pennsieve-dataset-"+str(dataId)+"-version-"+str(version)
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level == max_level: break
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))
            
## download dataset function
def get_dataset(dataId, version, dest_dir="."):
    """ Save a dataset from the SPARC data portal using the Pennsieve API.
    
    Inputs: 
    dataId -- integer id of the dataset
    version -- integer dataset version 
    dest_dir -- string directory to save data set into. Default is root.
    
    Outputs: 
    None 
    """
    url = "https://api.pennsieve.io/discover/datasets/"+str(dataId)+"/versions/"+str(version)+"/download?"
    # download dataset
    response = requests.get(url, stream = True)
    file_zip = "data.zip"
    data_file = open(file_zip,"wb")
    for chunk in tqdm(response.iter_content(chunk_size=1024)):
        data_file.write(chunk)
    data_file.close()
    # unzip dataset
    with ZipFile(file_zip, 'r') as obj:
       obj.extractall()
    # delete temporary zip file
    os.remove(file_zip)
    
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
    """ Extracts required fields from the data frame to prepare for projection to 3D scaffold faces
    
    Inputs: 
    df -- pandas dataframe with at least, x, y, area and face fields
    
    Outputs:
    data_2_dim -- Nx2 numpy array two-dimensional data coordinates for the neurons
    data_intensity -- Nx1 numpy array for the area of innervation of each neuron to encode colour intensity
    data_face -- the face ont which the neurons must be projected (D for dorsal, V for ventral)    
    """
    print(df)
    data_array = np.array(df[['y','z','area','face']])

    # Convert input data to numpy coordinate array and intensity array.
    data_2_dim = np.array(data_array[:, (0,1)])
    data_intensity = data_array[:,2]
    data_face = data_array[:, 3]
    
    return data_2_dim, data_intensity, data_face

def map_to_3D(input_pts, data_face, input_mesh):
    """ Maps an Nx2 numpy array of points in the y-z plane to have an
    x coordinate based on the nearest point in the y-z plane on the input mesh.

    Inputs:
    input_pts -- np.array(N, 2) with y coordinates in column 0, and
        z coordinates in column 1.
    data_face -- np.array(N,) of strings 'V' or 'D' indicating ventral or dorsal face respectively
    input_mesh -- numpy-stl mesh object with the target mesh.

    Outputs:
    out: np.array(N, 3), numpy array with x coordinates in column 0,
        y coordinates in column 1, and z coordinates in column 2.

    """
    # Create list of vertices from the vectors of each triangle in the mesh.
    vert = np.around(np.unique(input_mesh.vectors.reshape(
        [int(input_mesh.vectors.size/3), 3]), axis=0),2)

    # initial output array
    out = np.zeros((input_pts.shape[0], 3))

    # iterate over all points in y-z plane and find the closest mesh vertex in this plane
    for i, pt in enumerate(input_pts):
    
        if data_face[i] == 'V' or data_face[i] == 'Stomach - ventral':
            vert_candidate = vert[vert[:, 0] < 9.0, :]
            offset = 1
            jitter = 0.31
        else:
            vert_candidate = vert[vert[:, 0] > 8.7, :]
            offset = -1
            jitter = -0.31
            
        min_arg = np.argmin(np.sum(np.power(
            np.abs((pt-vert_candidate[:, 1:3])),2), 1))
        matched_x = vert_candidate[min_arg, 0]
        
        # Add some random movement so that triangles don't obscure points
        matched_x -= offset + np.random.rand()*jitter
        out[i, :] = [matched_x, pt[0], pt[1]]
    return out

## We are looking for vagal datasets so we create a query "vagal", returning 5 results using default value
search_dataset('vagal')

# ## The first three datasets are interesting so download them
# get_dataset(dataId=10, version=3)
# get_dataset(dataId=11, version=3)
# get_dataset(dataId=12, version=3)

# ## Exploring downloaded dataset. 
# ## We needs the derivative analysis result in derivative folder (we know this because we have inspected the dataset documentation in the manifest and README files)
# print_folder_structure(dataId=10, version=3)
# print_folder_structure(dataId=11, version=3)
# print_folder_structure(dataId=12, version=3)

# # copy the required files to res folder for further utilisation
# !mkdir res
# !mv Pennsieve-dataset-10-version-3/files/derivative/IGLE_data.xlsx res
# !mv Pennsieve-dataset-11-version-3/files/derivative/IMA_analyzed_data.xlsx res
# !mv Pennsieve-dataset-12-version-3/files/derivative/Efferent_data.xlsx res

# Setup maximimum y and z widths based on scale in image.
z_lims = [0, 36.7]
y_lims = [24.6, 0]

col_keeps = {'%x (distance from pylorus side)':'%x', '%y (distance from bottom)':'%y',
             'Average IGLE Area (um²)':'area', 'Area Of Innervation':'area', 
             'Neuron Area Of Innervation (um²) -Convex Hull':'area', 'V/D':'face',
             'specimen anatomical location':'face'}


df_igle = load_data('res/IGLE_data.xlsx', col_keeps, y_lims, z_lims)
df_ima = load_data('res/IMA_analyzed_data.xlsx', col_keeps, y_lims, z_lims)
df_efferent = load_data('res/Efferent_data.xlsx', col_keeps, y_lims, z_lims)

efferent_2D, efferent_intensity, efferent_face = convert_2D_data(df_efferent)
igle_2D, igle_intensity, igle_face = convert_2D_data(df_igle)
ima_2D, ima_intensity, ima_face = convert_2D_data(df_ima)

# Load the STL files and add the vectors to the plot
stomach_mesh = msh.Mesh.from_file('res/stom_surf_mesh.stl')

# with coordinate axes (imported with signs reversed)
stomach_mesh.x -= np.min(stomach_mesh.x.flatten())
stomach_mesh.y -= np.min(stomach_mesh.y.flatten())
stomach_mesh.z -= np.min(stomach_mesh.z.flatten())

# Project to 3D stomach surface.
efferent_3D = map_to_3D(efferent_2D, efferent_face, stomach_mesh, )
igle_3D = map_to_3D(igle_2D, igle_face, stomach_mesh)
ima_3D = map_to_3D(ima_2D, ima_face, stomach_mesh)

# Enable interactivity in jupyterlab.
# %matplotlib widget

def plotting_fct(mesh, efferent_3D, igle_3D, ima_3D, efferent_intensity,
                 igle_intensity, ima_intensity, efferent, igle, ima):
    # Start a matplotlib 3d interactive figure.
    fig = plt.figure()
    fig.suptitle('Projection visualisation', fontsize=16)
    ax = fig.add_subplot(projection='3d')

    # Add mesh as triangle polygons to 3d matplotlib view.
    faces = mplot3d.art3d.Poly3DCollection(mesh.vectors, color=(0.960, 0.803, 0.650))
    faces.set_edgecolor((0.960, 0.803, 0.650, 0.1))
    faces.set_alpha(0.1)
    ax.add_collection3d(faces)

    # Plot the projected neurons coloured by their area of innervation.
    if efferent:
        ax.scatter(efferent_3D[:,0], efferent_3D[:,1], efferent_3D[:,2],
                   c=efferent_intensity, cmap='Blues')

    if ima:
        ax.scatter(ima_3D[:,0], ima_3D[:,1], ima_3D[:,2],
                   c=ima_intensity, cmap='PuRd')

    if igle:
        ax.scatter(igle_3D[:,0], igle_3D[:,1], igle_3D[:,2],
                    c=igle_intensity, cmap='BuGn')


    # Scale view to the mesh size and turn off axis chrome.
    ax.set_xlim(0,40)
    ax.set_ylim(-10,30)
    ax.set_zlim(-10,30)
    ax.axis('off')

    # Show ventral surface and plot projected neurons.
    ax.view_init(10, -57, 'y')
    plt.show()

