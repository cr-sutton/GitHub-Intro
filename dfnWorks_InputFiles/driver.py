#   :synopsis: Driver run file for TPL example
#   :version: 2.0
#   :maintainer: Jeffrey Hyman
#.. moduleauthor:: Jeffrey Hyman <jhyman@lanl.gov>
#"""
from pydfnworks import *
import os
import sys
import re
import numpy as np

numPolygons = 12
src_path = os.getcwd()
jobname = f"{src_path}/output_graph"

DFN = DFNWORKS(jobname, ncpu=8)

DFN.params['domainSize']['value'] = [10, 10, 10]
DFN.params['h']['value'] = 0.1
DFN.params['tripleIntersections']['value'] = True
DFN.params['stopCondition'][
    'value'] = 0  #define stopCondition and nPoly for user polygons to avoid exception
DFN.params['nPoly']['value'] = numPolygons
DFN.params['ignoreBoundaryFaces']['value'] = True
DFN.params['disableFram']['value']=True
DFN.params['keepIsolatedFractures']['value']=True

DFN.add_user_fract_from_file(
    shape="poly",
    filename=f'{src_path}/polygons.dat',
    permeability=numPolygons * [1e-12],  #list or array of nPolygons perms
    nPolygons=numPolygons)

# build network
DFN.make_working_directory(delete=False)
DFN.check_input()
DFN.create_network()
r = np.sqrt(DFN.surface_area/np.pi)
#print(r)
DFN.aperture = 1E-4 * r **(1/2)
#print(DFN.aperture)
DFN.perm = DFN.aperture**2 / 12 
print(DFN.perm, DFN.aperture)

pressure_in = 2 * 10**6
pressure_out = 10**6
G = DFN.run_graph_flow("left", "right", pressure_in, pressure_out)
number_of_particles = 10000
  
DFN.run_graph_transport(G, number_of_particles, "graph_partime",
                          "graph_frac_sequence", format="ascii", initial_positions = 'flux')