"""
 Author: Param Deshpande
 Date created:  Wed Jun 24 22:52:06 IST 2020
 Description: 
 Used for showing live trajectory outputs of gimbal and buggy
 License :
 ------------------------------------------------------------
 "THE BEERWARE LICENSE" (Revision 42):
 Param Deshpande wrote this code. As long as you retain this 
 notice, you can do whatever you want with this stuff. If we
 meet someday, and you think this stuff is worth it, you can
 buy me a beer in return.
 ------------------------------------------------------------
 date modified:  Wed Jun 24 22:52:06 IST 2020
"""

#import 
#import 
import random
from itertools import count
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d

plt.style.use('fivethirtyeight')
fig = plt.figure()
ax = fig.add_subplot(2,1,1)
#ax2 = fig.add_subplot(2,1,2)
x_values = []   # time var
y_values = []   # Var 1
z_values = []   # Var 2
q_values = []   # Var 3
counter = 0
index = count()


new_value_status = False

#if __name__ == '__main__':
  #import 
  #import 

""" WRITE YOUR FUNCTIONS HERE """



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


def updateLive(y,z,q):
    """
    (float, float,float) -> (list, list, list)
    Description : Appends the output to y,z,q array  
    """
    y_values.append(y)
    z_values.append(z)
    q_values.append(q)
    new_value_status = True

#def ...:
#  """
#  () -> ()
#  Description: 
#  >>>
#  
#  """


def animate(i):
    
    #print(counter)
    

    x = next(index) # counter or x variable -> index
    counter = next(index)
    print(counter)
    x_values.append(x)
    '''
    Three random value series ->
    Y : 0-5
    Z : 3-8
    Q : 0-10
    '''
    while(new_value_status != True):
        pass
    new_value_status = False
    if counter >40:
        '''
        This helps in keeping the graph fresh and refreshes values after every 40 timesteps
        '''
        x_values.pop(0)
        y_values.pop(0)
        z_values.pop(0)
        q_values.pop(0)
        #counter = 0
        plt.cla() # clears the values of the graph
        
    plt.plot(x_values, y_values,linestyle='solid')
    plt.plot(x_values, z_values,linestyle='solid')
    plt.plot(x_values, q_values,linestyle='solid')
    
    ax.legend(["Value 1 ","Value 2","Value 3"])
    ax.set_xlabel("X values")
    ax.set_ylabel("Values for Three different variable")
    plt.title('Dynamic line graphs')
    
    time.sleep(.25) # keep refresh rate of 0.25 seconds

""" START YOUR CODE HERE """

def showGimbalTraj():
  updateLive(1,2,3)
  ani = FuncAnimation(plt.gcf(), animate, 1000)
  plt.tight_layout()
  plt.show()

if __name__ == '__main__':
  pass
  #import doctest
  #doctest.testmod()
  
  
  
  
""" END OF FILE """

