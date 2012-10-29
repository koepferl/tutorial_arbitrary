import numpy as np
from hyperion.model import Model
from hyperion.util.constants import au, lsun, rsun
from hyperion.dust import SphericalDust


# Model
m = Model()
dist = 20000 * au
x = np.linespace(-dist, dist, 11)
y = np.linespace(-dist, dist, 11)
z = np.linespace(-dist, dist, 11)
m.set_cartesian_grid(x,y,z)

# Dust
d = SphericalDust('kmh.hdf5')
d.set_sublimation_temperature('fast', temperature=1600.)
m.add_density_grid(np.ones((100,100,100)),'kmh.hdf5')

# Alpha centauri
sourceA = m.add_point_source()
sourceA.luminosity = 1.519 * lsun
sourceA.radius = 1.227 * rsun
sourceA.temperature = 5790.
sourceA.position = (0.,0., 0.)

# Beta centauri
sourceB = m.add_point_source()
sourceB.luminosity = 0.5 * lsun
sourceB.radius = 0.865 * rsun
sourceB.temperature = 5260.
sourceB.position = (-11.2 * dist,0., 0.)

# Proxima centauri
sourceP = m.add_point_source()
sourceP.luminosity = 0.0017 * lsun
sourceA.radius = 0.141 * rsun
sourceP.temperature = 3042.
sourceP.position = (0., 15000 * dist, 0.)

# Add 10 SEDs for different viewing angles
image = m.add_peeled_images(sed=True, image=False)
image.set_wavelength_range(250, 0.01, 5000.)
image.set_viewing_angles(np.linspace(0., 90., 10), np.repeat(20., 10))
image.set_track_origin('basic')

# Add multi-wavelength image for a single viewing angle
image = m.add_peeled_images(sed=False, image=True)
image.set_wavelength_range(30, 1., 1000.)
image.set_viewing_angles([30.], [20.])
image.set_image_size(200, 200)
image.set_image_limits(-dist, dist, -dist, dist)

# Add a fly-around at 500 microns
image = m.add_peeled_images(sed=False, image=True)
image.set_wavelength_range(1, 499., 501.)
image.set_viewing_angles(np.repeat(45., 36), np.linspace(5., 355., 36))
image.set_image_size(200, 200)
image.set_image_limits(-dist, dist, -dist, dist)

# Radiative Transfer
m.set_n_initial_iterations(5)
m.set_raytracing(True)
m.set_n_photons(initial=1000000, imaging=1000000,
                raytracing_sources=1000000, raytracing_dust=1000000)
m.set_sample_sources_evenly(True)

# Write out and run input file
m.write('input.rtin')
m.run('input.rtin', mpi=true, n_processes = 2)
