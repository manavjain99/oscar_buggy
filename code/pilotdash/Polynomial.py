"""
 Author: Param Deshpande
 Date created:  Sun Jul 12 14:39:20 IST 2020
 Description: 
 class polynomial for printing a spline from coeffs
 copied from https://www.python-course.eu/polynomial_class_in_python.php
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Sun Jul 12 14:39:20 IST 2020
"""

#import 
#import 
import numpy as np
import matplotlib.pyplot as plt


#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """

class Polynomial:
    
    def __init__(self, *coefficients):
        """ input: coefficients are in the form a_n, ...a_1, a_0 
        """
        self.coefficients = list(coefficients) # tuple is turned into a list
     
    def __repr__(self):
        """
        method to return the canonical string representation 
        of a polynomial.
   
        """
        return "Polynomial" + str(self.coefficients)
            
    def __call__(self, x):    
        res = 0
        for coeff in self.coefficients:
            res = res * x + coeff
        return res 
    
    def degree(self):
        return len(self.coefficients)   
            
    def __add__(self, other):
        c1 = self.coefficients[::-1]
        c2 = other.coefficients[::-1]
        res = [sum(t) for t in zip_longest(c1, c2, fillvalue=0)]
        return Polynomial(*res)
    
    def __sub__(self, other):
        c1 = self.coefficients[::-1]
        c2 = other.coefficients[::-1]
        
        res = [t1-t2 for t1, t2 in zip_longest(c1, c2, fillvalue=0)]
        return Polynomial(*res)
    
    def derivative(self):
        derived_coeffs = []
        exponent = len(self.coefficients) - 1
        for i in range(len(self.coefficients)-1):
            derived_coeffs.append(self.coefficients[i] * exponent)
            exponent -= 1
        return Polynomial(*derived_coeffs)
    
    def __str__(self):
        res = ""
        degree = len(self.coefficients) - 1
        res += str(self.coefficients[0]) + "x^" + str(degree)
        for i in range(1, len(self.coefficients)-1):
            coeff = self.coefficients[i]
            if coeff < 0:
                res += " - " +  str(-coeff) + "x^" + str(degree - i)
            else:
                res += " + " +  str(coeff) + "x^" + str(degree - i)
                
        if self.coefficients[-1] < 0:
            res += " - " + str(-self.coefficients[-1])
        else:
            res += " + " + str(self.coefficients[-1])

        return res

            

#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """


#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """


#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """

""" START YOUR CODE HERE """

if __name__ == '__main__':
  pass
  p = Polynomial(-0.8, 2.3, 0.5, 1, 0.2)

  p_der = p.derivative()

  X = np.linspace(-2, 3, 50, endpoint=True)

  F = p(X)
  F_derivative = p_der(X)
  plt.plot(X, F, label="F")
  plt.plot(X, F_derivative, label="F_der")

  plt.legend()
  plt.show()
  #import doctest
  #doctest.testmod()
  
  
  
  
""" END OF FILE """

