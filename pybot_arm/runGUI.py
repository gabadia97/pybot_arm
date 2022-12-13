import tkinter
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pybot_arm.pybot_ocp as ocp
import pybot_arm.pybot_plot as pbPlot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd
import tkinter.messagebox

from tkinter import *

#######################################################################################

win=Tk() #creating the main window and storing the window object in 'win'
win.title('pybot_arm') #set title of the window as pybot_arm
win.geometry('600x600') #set the size of the window

#function of the first button
#displays a welcome message
def func1():
    tkinter.messagebox.showinfo("Getting Started",
                                "Hello! Welcome to pybot_arm. Begin by entering some information about your system.")

#make the first button
btn1=Button(
    win,
    text="Click here to begin",
    width= 40, height= 5,
    command= func1,
    activeforeground='blue'
    ).place(x= 100, y= 0)

#function of the second button
#allows user to enter values for the length of robot arm and boundary values
def func2():
    
    #function of submit button
    #displays message when values are entered
    def printValue():
        
        length=float(ent1.get()) #first entry is length
        rho=float(ent2.get()) #second entry is for rho boundary values
        theta=float(ent3.get()) #third entry is for theta boundary values
        phi=float(ent4.get()) #fourth entry is for phi boundary values
        
        #put limits on user entries
        #length and rho must be positive
        #theta and phi must be between -2pi and 2pi
        if length>0 and rho>0 and abs(theta)<360 and abs(phi)<360:
            
            #if entries are within bounds, display a message
            #allowing user to continue to next step
            Label(win,
              text= f'Entered! Click perform calculations to continue.'
              ).place(x= 0, y= 500)
            
            #perform optimal control calculations
            def func4():
                N=int(ent1.get())
                length=float(ent2.get())
                rho_bound=float(ent3.get())
                theta_bound=float(ent4.get())*np.pi/180
                phi_bound=float(ent5.get())*np.pi/180
                
                bounds= {"rho": [rho_bound, rho_bound],
                         "rho_dot": [0,0],
                         "theta": [0,theta_bound],
                         "theta_dot": [0,0],
                         "phi": [phi_bound, phi_bound],
                         "phi_dot": [0,0]}
                
                sol = ocp.solve_pybot(N, length, bounds)
                ocp.export_to_csv(sol, "pybot_example")
                
                Label(win, text= f'View the spreadsheet "pybot_example.csv".').place(x= 0, y= 520)
                Label(win, 
                          text= f'See complete package for more detailed information and to view 3D animation.'
                          ).place(x= 0, y= 560)
                
            
            #create new button to perform calculations   
            btn4=Button(
                win,
                text="Perform Calculations",
                width=40, height=5,
                command=func4,
                activeforeground='blue'
                ).place(x= 100, y= 200)
        
        #if entries are not within bounds, have user start over
        else:
            Label(win,
              text= f'Invalid entry. Start over.'
              ).place(x= 0, y= 500)
    
    
            
    #user entry prompts
    Label(win,
          text='Enter number of points'
          ).place(x= 0, y= 400)
    Label(win,
          text='Enter length (in meters)'
          ).place(x= 0, y= 420) 
    Label(win,
          text='Enter boundary conditions for rho (in meters)'
          ).place(x= 0, y= 440)
    Label(win,
          text='Enter boundary conditions for theta (in degrees)'
          ).place(x= 0, y= 460)
    Label(win,
          text='Enter boundary conditions for phi (in degrees)'
          ).place(x= 0, y= 480)
    
    #entry blocks
    ent1= Entry(win) 
    ent2= Entry(win) 
    ent3= Entry(win)
    ent4= Entry(win)
    ent5= Entry(win)
    
    #location of entries
    ent1.place(x= 300, y= 400)
    ent2.place(x= 300, y= 420)
    ent3.place(x= 300, y= 440)
    ent4.place(x= 300, y= 460)
    ent5.place(x= 300, y= 480)
    
    #make third button
    btn3=Button(
    win,
    text="Submit", 
    command=printValue,
    activeforeground='blue'
    ).place(x= 350, y= 500)

#make second button   
btn2=Button(
    win,
    text="Enter information about your system",
    width=40, height=5,
    command=func2,
    activeforeground='blue'
    ).place(x= 100, y= 100)


win.mainloop() #running the loop that works as a trigger

