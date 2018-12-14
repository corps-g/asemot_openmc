# Fuel Assembly Example

import openmc
import openmc.mgxs as mgxs

import matplotlib.pyplot as plt
import h5py
import numpy as np

  
#%% Materials
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
       
#%% Geometry
pitch = 1.26
boundary = 'reflective'
left   = openmc.XPlane(x0=-pitch*2, boundary_type=boundary)
right  = openmc.XPlane(x0=pitch*2, boundary_type=boundary)
bottom = openmc.YPlane(y0=-pitch*2, boundary_type=boundary)
top    = openmc.YPlane(y0=pitch*2, boundary_type=boundary)
fuel_outer = openmc.ZCylinder(R=0.41)
clad_outer = openmc.ZCylinder(R=0.48)

# fuel-pin cells
fuel = openmc.Cell(1, 'fuel')
fuel.fill = uo2
fuel.region = -fuel_outer

cladding = openmc.Cell(2, 'cladding')
cladding.fill = zirconium #
cladding.region = +fuel_outer & -clad_outer

coolant = openmc.Cell(3, 'coolant')
coolant.fill = h2o
coolant.region = +clad_outer

# coolant channel cell (just a coolant square bigger than the pin cell)
coolant_channel = openmc.Cell(4, 'coolant_channel')
coolant_channel.fill = h2o
coolant_channel.region = +left & -right & +bottom & -top

# fuel-pin universe
univ_f = openmc.Universe(cells=[fuel, cladding, coolant], universe_id=1)

# coolant-channel universe
univ_c = openmc.Universe(cells=[coolant_channel], universe_id=2)

# 2-D lattice
lattice2d = openmc.RectLattice(lattice_id=5)
lattice2d.lower_left = [-2*pitch, -2*pitch]
lattice2d.pitch = [pitch, pitch]
lattice2d.universes = [[univ_f, univ_f, univ_f, univ_f],
                       [univ_f, univ_c, univ_f, univ_f],
                       [univ_f, univ_f, univ_f, univ_f],
                       [univ_f, univ_f, univ_f, univ_f]]

# encompassing cell
lattice_cell = openmc.Cell(cell_id=999)
lattice_cell.region = +left & -right & +bottom & -top
lattice_cell.fill = lattice2d

# root universe
root = openmc.Universe(universe_id=0, name='root universe')
root.add_cells([lattice_cell])
geom = openmc.Geometry(root)
geom.export_to_xml()

# plot
p = openmc.Plot()
p.filename = 'pinplot'
p.width = (4*1.26, 4*1.26)
p.pixels = (300, 300)
p.color_by = 'material'
plots = openmc.Plots([p])
plots.export_to_xml()
openmc.plot_geometry()
openmc.plot_inline(p)


#%% Tallies

# energy bins
energy_filter = openmc.EnergyFilter([0.0, 0.625, 2.0e7])

# tally flux over whole geometry
flux_tally = openmc.Tally(tally_id=1)
flux_tally.filters = [energy_filter]
flux_tally.scores = ['flux']


# tally mesh
mesh = openmc.Mesh(mesh_id=1)
mesh.type = 'regular'
mesh.dimension = [4, 4, 1]
mesh.lower_left = [-2*pitch, -2*pitch, -1e7]
mesh.width = [pitch, pitch, 2e7]
mesh_filter = openmc.MeshFilter(mesh)
mesh_tally = openmc.Tally(tally_id=2)
mesh_tally.filters = [mesh_filter]
mesh_tally.scores = ['fission']

# export to file
tallies_file = openmc.Tallies([flux_tally, mesh_tally])
tallies_file.export_to_xml()

#%% Settings
settings = openmc.Settings()
settings.batches = 100
settings.inactive = 10
settings.particles = 1000
settings.export_to_xml()

#%% Run and view
openmc.run(threads=1)

