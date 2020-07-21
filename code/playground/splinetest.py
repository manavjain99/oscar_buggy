#https://stackoverflow.com/questions/52393145/create-bspline-from-knots-and-coefficients
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline, LSQUnivariateSpline

x = np.linspace(0, 10, 50) # x-data
y = np.exp(-(x-5)**2/4)    # y-data

# define the knot positions

t = [1, 2, 4, 5, 6, 8, 9]

# get spline fit

s1 = LSQUnivariateSpline(x, y, t)

x2 = np.linspace(0, 10, 200) # new x-grid
y2 = s1(x2) # evaluate spline on that new grid

# FAILED: try to construct BSpline using the knots and coefficients
"""
k = s1.get_knots()
c = s1.get_coeffs()
s2 = BSpline(t,c,2)
"""
#correct version 
kn = s1.get_knots()
kn = 3*[kn[0]] + list(kn) + 3*[kn[-1]]
c = s1.get_coeffs()
print(c)
s2 = BSpline(kn, c, 3)    # not "2" as in your sample; we are working with a cubic spline 
# plotting

plt.plot(x, y, label='original')
plt.plot(t, s1(t),'o', label='knots')
plt.plot(x2, y2, '--', label='spline 1')
plt.plot(x2, s2(x2), 'r:', label='spline 2') 
plt.legend()
plt.show()