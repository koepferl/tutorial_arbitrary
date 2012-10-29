import numpy as np
import matplotlib.pyplot as plt

from hyperion.model import ModelOutput
from hyperion.util.constants import pc, au

dist = 20000 * au

# Read in the model
m = ModelOutput('input.rtout')

# Extract the quantities
g = m.get_quantities()

# Get the wall positions in pc
xw, yw = g.x_wall / dist, g.y_wall / dist

# Make a 2-d grid of the wall positions (used by pcolormesh)
X, Y = np.meshgrid(xw, yw)

# Calculate the density-weighted temperature
weighted_temperature =  np.sum(g['temperature'][0].array \
                               * g['density'][0].array, axis=2)\
                        / np.sum(g['density'][0].array, axis=2)

# Make the plot
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
c = ax.pcolormesh(X, Y, weighted_temperature)
ax.set_xlim(xw[0], xw[-1])
ax.set_xlim(yw[0], yw[-1])
ax.set_xlabel('x (20000 au)')
ax.set_ylabel('y (20000 au)')
cb = fig.colorbar(c)
cb.set_label('Temperature (K)')
fig.savefig('weighted_temperature_cartesian100.png', bbox_inches='tight')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
c = ax.pcolormesh(X, Y, g['temperature'][0].array[:, 5, :])
ax.set_xlim(xw[0], xw[-1])
ax.set_xlim(yw[0], yw[-1])
ax.set_xlabel('x (20000 au)')
ax.set_ylabel('y (20000 au)')
cb = fig.colorbar(c)
cb.set_label('Temperature (K)')
fig.savefig('sliced_temperature_cartesian100.png', bbox_inches='tight')
