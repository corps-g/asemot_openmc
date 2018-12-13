# Pin Cell Example

import openmc
import matplotlib.pyplot as plt
import h5py
import numpy as np

def make_xml():
    
    # MATERIALS
    uo2 = openmc.Material(1, "uo2")
    uo2.add_nuclide('U235', 0.04)
    uo2.add_nuclide('U238', 0.96)
    uo2.add_nuclide('O16', 2.0)
    uo2.set_density('g/cm3', 10.0)
    
    zirconium = openmc.Material(2, "zirconium")
    zirconium.add_element('Zr', 1.0)
    zirconium.set_density('g/cm3', 6.6)
        
    h2o = openmc.Material(3, "h2o")
    h2o.add_nuclide('H1', 2.0)
    h2o.add_nuclide('O16', 1.0)
    h2o.set_density('g/cm3', 1.0)
    h2o.add_s_alpha_beta('c_H_in_H2O')
    
    mats = openmc.Materials()
    mats += [uo2, zirconium, h2o]
    mats.export_to_xml()
        
    # GEOMETRY   
    pitch = 1.26
    left = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
    right = openmc.XPlane(x0=pitch/2, boundary_type='reflective')
    bottom = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
    top = openmc.YPlane(y0=pitch/2, boundary_type='reflective')
    fuel_outer = openmc.ZCylinder(R=0.41)
    clad_outer = openmc.ZCylinder(R=0.48)
    
    fuel = openmc.Cell(1, 'fuel')
    fuel.fill = uo2
    fuel.region = -fuel_outer
    
    cladding = openmc.Cell(2, 'cladding')
    cladding.fill = zirconium #
    cladding.region = +fuel_outer & -clad_outer
    
    coolant = openmc.Cell(3, 'coolant')
    coolant.fill = h2o
    coolant.region = +left & -right & +bottom & -top & +clad_outer
    
    root = openmc.Universe(cells=(fuel, cladding, coolant))
    geom = openmc.Geometry(root)
    geom.export_to_xml()
    
    # SETTINGS
    settings = openmc.Settings()
    settings.batches = 100
    settings.inactive = 10
    settings.particles = 1000
    settings.export_to_xml()

if __name__ == '__main__':
    
    #%% Make the XML files
    make_xml()
    
    #%% Run OpenMC
    openmc.run()
    
    #%% View output
    f = h5py.File('statepoint.100.h5', 'r') 
    print(list(f['/k_combined']))
    f.close()
    
    #%% Visualize geometry
    p = openmc.Plot()
    p.filename = 'pinplot'
    p.width = (1.26, 1.26)
    p.pixels = (300, 300)
    p.color_by = 'material'
    plots = openmc.Plots([p])
    plots.export_to_xml()
    openmc.plot_geometry()
    openmc.plot_inline(p)
