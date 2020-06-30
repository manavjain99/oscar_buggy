import random
from itertools import count
import time
import matplotlib.pyplot as plt
import queue
import threading
import concurrent.futures


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

#y_values.append(0)
#z_values.append(0)
#q_values.append(0)

new_value_status = [False]

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

    RPY_Q = queue.Queue(maxsize = 100)
    new_value_status = [True]
    print(new_value_status)
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
    print("plotting alive")
    #print(new_value_status)
    #while(new_value_status != True):
    #    #time.sleep(.25) # keep refresh rate of 0.25 seconds
    #    print("struck in while loop")
    #    print(new_value_status)
#
    #    pass
    ##new_value_status = False
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
    
    #time.sleep(.25) # keep refresh rate of 0.25 seconds


def update_thread():
    while(1):
        update_vals(y_values,z_values,q_values)
        print("Update thread alive")


def show_thread():
    print("Show thread alive")
    ani = FuncAnimation(plt.gcf(), animate, 1000)
    plt.tight_layout()
    plt.show()

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    executor.submit(show_thread)

#update_vals(y_values,z_values,q_values)
while(1):
    print("reached end of file")
    break

