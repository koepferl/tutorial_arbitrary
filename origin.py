import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from hyperion.model import ModelOutput
from hyperion.util.constants import pc

m = ModelOutput('input.rtout')

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Direct stellar photons
wav, nufnu = m.get_sed(inclination=0, aperture=-1, distance=300 * pc,
                       component='source_emit')
ax.loglog(wav, nufnu, color='blue')

# Scattered stellar photons
wav, nufnu = m.get_sed(inclination=0, aperture=-1, distance=300 * pc,
                       component='source_scat')
ax.loglog(wav, nufnu, color='teal')

# Direct dust photons
wav, nufnu = m.get_sed(inclination=0, aperture=-1, distance=300 * pc,
                       component='dust_emit')
ax.loglog(wav, nufnu, color='red')

# Scattered dust photons
wav, nufnu = m.get_sed(inclination=0, aperture=-1, distance=300 * pc,
                       component='dust_scat')
ax.loglog(wav, nufnu, color='orange')

ax.set_xlabel(r'$\lambda$ [$\mu$m]')
ax.set_ylabel(r'$\lambda F_\lambda$ [ergs/s/cm$^2$]')
ax.set_xlim(0.1, 10000.)
ax.set_ylim(1.e-40, 2.e-1)
fig.savefig('sed_origin100.png')