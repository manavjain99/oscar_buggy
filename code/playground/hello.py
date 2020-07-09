from tkinter import *
from PIL import ImageTk,Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
cam = cv2.VideoCapture(0)
root = Tk()
root.title('This is the First code for our GUI!')
root.geometry("400x200")
def graph():
    house1 = np.random.normal(200000, 25000, 5000)
    plt.figure(1)
    plt.hist(house1, 50)
    plt.show()
def graph1():
    house1 = np.random.normal(200000, 25000, 5000)
    plt.figure(2)
    plt.hist(house1, 50)
    plt.show()
def graph2():
    house1 = np.random.normal(200000, 25000, 5000)
    plt.figure(3)
    plt.hist(house1, 50)
    plt.show()
def newt():
    count = 0
    while True:
        ret, img = cam.read()
        cv2.imshow("Test", img)
        if not ret:
            break
        k=cv2.waitKey(1)
        if k%256==27:
            #for Esc key
            print("Close")
            break
        elif k%256==32:
            #for Space Key
            print("Image"+str(count)+"saved")
            file='C:/Users/Omkar Gaikwad/Desktop/helllo/img'+str(count)+'.jpg'
            cv2.imwrite(file, img)
            count +=1
my_button = Button(root, text="Graph It!1", command=graph)
my = Button(root, text="Graph It!2", command=graph1)
my_t = Button(root, text="Graph It3!", command=graph2)
mat = Button(root, text="CAM", command=newt)
my_button.pack()
my.pack()
my_t.pack()
mat.pack()
cam.release
cv2.destroyAllWindows
root.mainloop()
