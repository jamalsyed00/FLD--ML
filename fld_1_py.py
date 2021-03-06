# -*- coding: utf-8 -*-
"""FLD_1.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zWABXFH97soMUvsBtJgaKunHAEbW8ZL4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from mpl_toolkits.mplot3d import Axes3D

df=pd.read_csv("dataset_FLD.csv")

b1 = df[df.iloc[:, -1] == 1]
b0 = df[df.iloc[:, -1] == 0]

def plot3d(data):
    x=data.iloc[:,0]
    y=data.iloc[:,1]
    z=data.iloc[:,2]

    fg = plt.figure(figsize= (10, 7))
    ay = fg.add_subplot(111, projection='3d')

    ay.scatter(x, y, z, c=data.iloc[:,-1], cmap="seismic", alpha= 0.6)
    ay.set_xlabel("X")
    ay.set_ylabel("Y")
    ay.set_zlabel("Z")
    ay.set_xlim(-5,5)
    ay.set_ylim(-3,3)
    ay.set_zlim(-5,5)

    plt.show()

fg = plt.figure(figsize= (8, 6))
ay = fg.add_subplot(111, projection='3d')

x=b1.iloc[:,0]
y=b1.iloc[:,1]
z=b1.iloc[:,2]


ay.scatter(x, y, z, color= 'red', alpha= 0.6)
ay.set_xlabel("X")
ay.set_ylabel("Y")
ay.set_zlabel("Z")
ay.set_xlim(-5,5)
ay.set_ylim(-3,3)
ay.set_zlim(-5,5)

plt.show()

fg = plt.figure(figsize= (8, 6))
ay = fg.add_subplot(111, projection='3d')

x=b0.iloc[:,0]
y=b0.iloc[:,1]
z=b0.iloc[:,2]


ay.scatter(x, y, z, color= 'blue', alpha= 0.6)
ay.set_xlabel("X")
ay.set_ylabel("Y")
ay.set_zlabel("Z")
ay.set_xlim(-5,5)
ay.set_ylim(-3,3)
ay.set_zlim(-5,5)

plt.show()

plot3d(df)

def sol(u1,u2,s1,s2):
    # function to obtain roots
    a = 1/(2*s1**2) - 1/(2*s2**2)
    b = u2/(s2**2) - u1/(s1**2)
    c = u1**2 /(2*s1**2) - u2**2 / (2*s2**2) - np.log(s2/s1)
    d = np.roots([a,b,c])
    r=0
    for i in d:
        if u2<i and i<u1:
            r=i
    return r

def LDA(data):
    b1=data[data.iloc[:,3]==1] 
    b1=b1.iloc[:, [0,1,2]]
    u1=b1.mean(axis=0)
    sub1=b1-u1
    b2=data[data.iloc[:,3]==0]
    b2=b2.iloc[:, [0,1,2]]
    u2=b2.mean(axis=0)
    sub2=b2-u2
    mean=u2-u1
    #to print the mean

    sc1=np.dot(np.transpose(sub1),sub1)  #1st scatter matrix
    #to print the scatter matrix 
    
    sc2=np.dot(np.transpose(sub2),sub2)  #2nd scatter matrix
    #to print the scatter matrix
    
    sw=np.add(sc1,sc2)                                   #adding the 2 scatter matrices
    

    swinv=np.linalg.inv(sw)                        #inverse of sw
    

    w=np.dot(swinv,u1-u2)           
    
    
    projb1=np.dot(w,np.transpose(b1))   #projection of class 1
    projc0=np.dot(w,np.transpose(b2))   #projection of class 0

    # caluculation of avg and std for each class
    av1=projb1.mean()
    s1=projb1.std()

    av2=projc0.mean()
    s2=projc0.std()
    
    x_all = np.arange(-0.05, 0.05, 0.001)
    y1=norm.pdf(x_all,av1,s1)
    y0=norm.pdf(x_all,av2,s2)

    result = sol(av1,av2,s1,s2) #the value which seperates bw the classes 
    
    plt.figure(4)
    plt.plot(x_all,y0,c='black',label="class 0")
    plt.hist(projc0,bins=12,color="#2d7af7")
    plt.xlabel("projection line",fontsize="10")
    plt.ylabel("density of points",fontsize="10")
    plt.xlim(-0.075, 0.075)
    plt.ylim(0,125)
    plt.legend()
    plt.show()
    
    plt.figure(3)
    plt.plot(x_all,y1,c='black',label="class 1")
    plt.hist(projb1,bins=25,color="#b32e42")
    plt.xlabel("projection line",fontsize="10")
    plt.ylabel("density of points",fontsize="10")
    plt.xlim(-0.075, 0.075)
    plt.ylim(0,125)
    plt.legend()
    plt.show()
    
    plt.figure(2)
    plt.plot(x_all,y1,c='black',label="class 1")
    plt.hist(projb1,bins=25,color="#b32e42")
    plt.plot(x_all,y0,c='black',label="class 0")
    plt.hist(projc0,bins=12,color="#2d7af7")
    plt.xlabel("projection line",fontsize="10")
    plt.ylabel("density of points",fontsize="10")
    yp= np.linspace(-0.03,0.03,1000)
    xp=result*np.ones((1000))
    #pery_vals = c + per * perx_vals
    plt.plot(xp, yp*1000, '-')
    plt.xlim(-0.075, 0.075)
    plt.ylim(0,125)
    plt.legend()
    plt.show()
    
    
      

    #ploting the projected points
    plt.figure(1)
    yp=0*projb1
    plt.scatter(projb1,yp,c='#b32e42',label="class 1")
    yp=0*projc0
    plt.scatter(projc0,yp,c='#2d7af7',label="class 0")
    yp= np.linspace(-0.03,0.03,1000)
    xp=result*np.ones((1000))
    #pery_vals = c + per * perx_vals
    plt.plot(xp, yp*1000, '-')  
    plt.xlim(-0.075, 0.075)
    plt.ylim(-0.1,0.1)

    pdf1 = norm.pdf(b1, av1, s1)

    pdf2 = norm.pdf(b2, av2, s2)
    plt.show()
    

    return w,result

W, result = LDA(df)

normal = W
point = result
x=df.iloc[:,0]
y=df.iloc[:,1]
z=df.iloc[:,2]

fg = plt.figure(figsize=(10,8))
ay = fg.add_subplot(111, projection='3d')
ay.scatter(x,y,z,c=df.iloc[:,3],cmap="seismic")
ay.set_xlabel("X")
ay.set_ylabel("Y")
ay.set_zlabel("Z")
ay.set_xlim(-10,10)
ay.set_ylim(-3,3)
ay.set_zlim(-2,2)

# create x,y
xx, yy = np.meshgrid(range(-10,11), range(-3,4))

# calculate corresponding z
z = (-normal[0] * xx - normal[1] * yy - point) * 1. /normal[2]

# plot the surface
ay.plot_surface(xx, yy, z, alpha=0.2, color= '#56d160')
plt.show()