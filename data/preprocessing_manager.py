import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, griddata

# ------------------------------ 1D INTERPOLATION ------------------------------
x = np.linspace(0, 10, num=11, endpoint=True)
y = np.cos(-x**2/9.0)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='cubic')

xnew = np.linspace(0, 10, num=41, endpoint=True)

plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()

# ------------------------------ MULTIVARIATE DATA INTERPOLATION ------------------------------


def func(x, y):
    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2


def interpolation(points):
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

    points = np.random.rand(1000, 2)
    values = func(points[:, 0], points[:, 1])

    grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
    grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

    plt.subplot(221)
    plt.imshow(func(grid_x, grid_y).T, extent=(0, 1, 0, 1), origin='lower')
    plt.plot(points[:,0], points[:, 1], 'k.', ms=1)
    plt.title('Original')
    plt.subplot(222)
    plt.imshow(grid_z0.T, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Nearest')
    plt.subplot(223)
    plt.imshow(grid_z1.T, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Linear')
    plt.subplot(224)
    plt.imshow(grid_z2.T, extent=(0, 1, 0, 1), origin='lower')
    plt.title('Cubic')
    plt.gcf().set_size_inches(6, 6)
    plt.show()

# grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]
#
# points = np.random.rand(1000, 2)
# values = func(points[:, 0], points[:, 1])
#
# grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
# grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
# grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')
#
# plt.subplot(221)
# plt.imshow(func(grid_x, grid_y).T, extent=(0, 1, 0, 1), origin='lower')
# plt.plot(points[:,0], points[:, 1], 'k.', ms=1)
# plt.title('Original')
# plt.subplot(222)
# plt.imshow(grid_z0.T, extent=(0, 1, 0, 1), origin='lower')
# plt.title('Nearest')
# plt.subplot(223)
# plt.imshow(grid_z1.T, extent=(0, 1, 0, 1), origin='lower')
# plt.title('Linear')
# plt.subplot(224)
# plt.imshow(grid_z2.T, extent=(0, 1, 0, 1), origin='lower')
# plt.title('Cubic')
# plt.gcf().set_size_inches(6, 6)
# plt.show()