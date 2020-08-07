import numpy as np
#import scipy
import scipy.interpolate
import matplotlib.pyplot as plt

"""
The following code in comments was used to generate splines from Coeffs, 
Run by splineplot.py in pilot dash the coeffs were adde to Splinecoeffs in format 
time d c b a / or ( ab b c d ) simply compy pasted the Output for now 
"""

# calculate 5 natural cubic spline polynomials for 6 points
# (x,y) = (0,12) (1,14) (2,22) (3,39) (4,58) (5,77)
x = np.array([0, 1, 2, 3, 4, 5])
y = np.array([12,14,22,39,58,77])

# show values of interpolation function at x=1.25

#tck = scipy.interpolate.splrep(x, y)
#pp = scipy.interpolate.interpolate.spltopp(tck[0][1:-1], tck[1], tck[2])
#print(pp.coeffs.T)
# send c4,c3,c2s to stm and interpolate according to those vals.    
# Split those vals in stm according to the timestamps. 

# Cubic spline interpolation calculus example
#  https://www.youtube.com/watch?v=gT7F3TWihvk
"""
Python 3.8.3 (default, May 17 2020, 18:15:42) 
[GCC 10.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import matplotlib.pyplot as plt
>>> from scipy.interpolate import splev, splrep
>>> x = np.linspace(0, 10, 10)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>> import numpy as np
>>> x = np.linspace(0, 10, 10)
>>> y = np.sin(x)
>>> spl = splrep(x, y)
>>> x2 = np.linspace(0, 10, 200)
>>> y2 = splev(x2, spl)
>>> plt.plot(x, y, 'o', x2, y2)
[<matplotlib.lines.Line2D object at 0x7f09e667ef10>, <matplotlib.lines.Line2D object at 0x7f09e667e2e0>]
>>> plt.show()
>>> spl
(array([ 0.        ,  0.        ,  0.        ,  0.        ,  2.22222222,
        3.33333333,  4.44444444,  5.55555556,  6.66666667,  7.77777778,
       10.        , 10.        , 10.        , 10.        ]), array([-4.94881722e-18,  8.96543619e-01,  1.39407154e+00, -2.36640266e-01,
       -1.18324030e+00, -8.16301228e-01,  4.57836125e-01,  1.48720677e+00,
        1.64338775e-01, -5.44021111e-01,  0.00000000e+00,  0.00000000e+00,
        0.00000000e+00,  0.00000000e+00]), 3)
>>> spl.shape
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'shape'
>>> spl.shape()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'shape'
>>> spl.dim()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'dim'
>>> type(spl)
<class 'tuple'>
>>> tck = splrep(x, y)
>>> import scipy
>>> pp = PPoly.from_spline(tck)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'PPoly' is not defined
>>> from scipy.interpolate import PPoly, splrep
>>> pp = PPoly.from_spline(tck)
>>> pp.c.T
array([[-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [ 1.72952212e-01, -4.64551679e-01, -5.84561936e-01,
         7.95220057e-01],
       [ 1.26008293e-01,  1.11955696e-01, -9.76335250e-01,
        -1.90567963e-01],
       [-4.93704109e-02,  5.31983340e-01, -2.60847433e-01,
        -9.64317117e-01],
       [-1.71230879e-01,  3.67415303e-01,  7.38484392e-01,
        -6.65101515e-01],
       [-1.08680287e-01, -2.03354294e-01,  9.20774403e-01,
         3.74151231e-01],
       [ 1.00658224e-01, -5.65621916e-01,  6.63563923e-02,
         9.97097891e-01],
       [ 1.00658224e-01,  1.05432909e-01, -9.56285846e-01,
        -5.44021111e-01],
       [ 1.00658224e-01,  1.05432909e-01, -9.56285846e-01,
        -5.44021111e-01],
       [ 1.00658224e-01,  1.05432909e-01, -9.56285846e-01,
        -5.44021111e-01]])
>>> type(pp.c.T)
<class 'numpy.ndarray'>
>>> (pp.c.T).shape()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object is not callable
>>> theArr = pp.c.T
>>> theArr.shape()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object is not callable
>>> theArr.ndim   
2
>>> theArr
array([[-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [-1.82100357e-02, -3.43151441e-01,  1.21033389e+00,
        -4.94881722e-18],
       [ 1.72952212e-01, -4.64551679e-01, -5.84561936e-01,
         7.95220057e-01],
       [ 1.26008293e-01,  1.11955696e-01, -9.76335250e-01,
        -1.90567963e-01],
       [-4.93704109e-02,  5.31983340e-01, -2.60847433e-01,
        -9.64317117e-01],
       [-1.71230879e-01,  3.67415303e-01,  7.38484392e-01,
        -6.65101515e-01],
       [-1.08680287e-01, -2.03354294e-01,  9.20774403e-01,
         3.74151231e-01],
       [ 1.00658224e-01, -5.65621916e-01,  6.63563923e-02,
         9.97097891e-01],
       [ 1.00658224e-01,  1.05432909e-01, -9.56285846e-01,
        -5.44021111e-01],
       [ 1.00658224e-01,  1.05432909e-01, -9.56285846e-01,
        -5.44021111e-01],
       [ 1.00658224e-01,  1.05432909e-01, -9.56285846e-01,
        -5.44021111e-01]])
>>> 

"""