import matplotlib.pyplot as plt

from floras_helpers import plotting


fig,ax = plt.subplots(1,1)

ax.plot(range(5))
plotting.off_axes(ax)

plt.show()