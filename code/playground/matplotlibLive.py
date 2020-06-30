import random
from itertools import count
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
plt.style.use('fivethirtyeight')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ax2 = fig.add_subplot(2,1,2)
x_values = []   # time var
y_values = []   # Var 1
z_values = []   # Var 2
q_values = []   # Var 3
counter = 0
index = count()

def update_vals(y_values,z_values,q_values):
    """
    (list, list, list) -> NoneType
    Description : Appends vals to the three arrays passed 
    """
    y = random.randint(0, 5)
    z = random.randint(3, 8)
    q = random.randint(0, 10)
    # append values to keep graph dynamic
    # this can be replaced with reading values from a csv files also
    # or reading values from a pandas dataframe
    y_values.append(y)
    z_values.append(z)
    q_values.append(q)
    

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
    update_vals(y_values,z_values,q_values)
    
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
    
    ax.legend(["Roll ","Pitch ","Yaw"])
    ax.set_xlabel("Time (unform and unscaled)")
    ax.set_ylabel("Values for Three different variable")
    plt.title('Dynamic line graphs')
    
    time.sleep(.25) # keep refresh rate of 0.25 seconds

ani = FuncAnimation(plt.gcf(), animate, 1000)
plt.tight_layout()
plt.show()

