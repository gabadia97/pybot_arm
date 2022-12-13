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
import tkinter.messagebox

from tkinter import *

win=Tk() #creating the main window and storing the window object in 'win'
win.title('pybot_arm') #set title of the window as pybot_arm
win.geometry('500x680') #set the size of the window

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
        
        N=int(ent1.get())
        length=float(ent2.get()) 
        rho0=float(ent3.get()) #rho initial value
        rhof=float(ent4.get()) #rho final value
        theta0=float(ent5.get()) #theta initial value
        thetaf=float(ent6.get()) #theta final value
        phi0=float(ent7.get()) #phi initial value
        phif=float(ent8.get()) #phi final value
        rhodot0=float(ent9.get()) #rho initial value
        rhodotf=float(ent10.get()) #rho final value
        thetadot0=float(ent11.get()) #theta initial value
        thetadotf=float(ent12.get()) #theta final value
        phidot0=float(ent13.get()) #phi initial value
        phidotf=float(ent14.get()) #phi final value
        
        #put limits on user entries
        #length and rho must be positive
        #theta and phi must be between -2pi and 2pi
        if length>0 and rho0>0 and abs(theta0)<360 and abs(phi0)<360:
            
            #if entries are within bounds, display a message
            #allowing user to continue to next step
            Label(win,
              text= f'Entered! Click perform calculations to continue.'
              ).place(x= 0, y= 580)
            
            #perform optimal control calculations
            def func4():
                
                N=int(ent1.get())
                length=float(ent2.get()) 
                rho0=float(ent3.get()) #rho initial value
                rhof=float(ent4.get()) #rho final value
                theta0=float(ent5.get())*np.pi/180 #theta initial value
                thetaf=float(ent6.get())*np.pi/180 #theta final value
                phi0=float(ent7.get())*np.pi/180 #phi initial value
                phif=float(ent8.get())*np.pi/180 #phi final value
                rhodot0=float(ent9.get()) #rho initial value
                rhodotf=float(ent10.get()) #rho final value
                thetadot0=float(ent11.get())*np.pi/180 #theta initial value
                thetadotf=float(ent12.get())*np.pi/180 #theta final value
                phidot0=float(ent13.get())*np.pi/180 #phi initial value
                phidotf=float(ent14.get())*np.pi/180 #phi final value
                
                
                
                #N=int(ent1.get())
                #length=float(ent2.get())
                #rho_bound=float(ent3.get())
                #theta_bound=float(ent4.get())*np.pi/180
                #phi_bound=float(ent5.get())*np.pi/180
                
                bounds= {"rho": [rho0, rhof],
                         "rho_dot": [rhodot0,rhodotf],
                         "theta": [theta0,thetaf],
                         "theta_dot": [thetadot0,thetadotf],
                         "phi": [phi0, phif],
                         "phi_dot": [phidot0,phidotf]}
                
                sol = ocp.solve_pybot(N, length, bounds)
                ocp.export_to_csv(sol, "pybot_example")
                
                Label(win, text= f'View the spreadsheet "pybot_example.csv".').place(x= 0, y= 600)
                Label(win, 
                          text= f'See complete package for more detailed information and to view 3D animation.'
                          ).place(x= 0, y= 620)
                
            
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
              ).place(x= 0, y= 580)
        
    #user entry prompts
    Label(win,
          text='Enter number of points'
          ).place(x= 0, y= 300)
    Label(win,
          text='Enter length (in meters)'
          ).place(x= 0, y= 320) 
    Label(win,
          text='Enter initial condition for rho (in meters)'
          ).place(x= 0, y= 340)
    Label(win,
          text='Enter final condition for rho (in meters)'
          ).place(x= 0, y= 360)
    Label(win,
          text='Enter initial condition for theta (in degrees)'
          ).place(x= 0, y= 380)
    Label(win,
          text='Enter final condition for theta (in degrees)'
          ).place(x= 0, y= 400)
    Label(win,
          text='Enter initial condition for phi (in degrees)'
          ).place(x= 0, y= 420)
    Label(win,
          text='Enter final conditions for phi (in degrees)'
          ).place(x= 0, y= 440)
    Label(win,
          text='Enter initial conditions for rho_dot (in m/s)'
          ).place(x= 0, y= 460)
    Label(win,
          text='Enter final condition for rho_dot (in m/s)'
          ).place(x= 0, y= 480)
    Label(win,
          text='Enter initial conditions for theta_dot (in degrees/s)'
          ).place(x= 0, y= 500)
    Label(win,
          text='Enter final condition for theta_dot (in degrees/s)'
          ).place(x= 0, y= 520)
    Label(win,
          text='Enter initial conditions for phi_dot (in degrees/s)'
          ).place(x= 0, y= 540)
    Label(win,
          text='Enter final condition for phi_dot (in degrees/s)'
          ).place(x= 0, y= 560)
      
    #entry blocks
    ent1= Entry(win) 
    ent2= Entry(win) 
    ent3= Entry(win)
    ent4= Entry(win)
    ent5= Entry(win)
    ent6= Entry(win) 
    ent7= Entry(win)
    ent8= Entry(win)
    ent9= Entry(win)
    ent10= Entry(win) 
    ent11= Entry(win)
    ent12= Entry(win)
    ent13= Entry(win)
    ent14= Entry(win)
    
    #location of entries
    ent1.place(x= 300, y= 300)
    ent2.place(x= 300, y= 320)
    ent3.place(x= 300, y= 340)
    ent4.place(x= 300, y= 360)
    ent5.place(x= 300, y= 380)
    ent6.place(x= 300, y= 400)
    ent7.place(x= 300, y= 420)
    ent8.place(x= 300, y= 440)
    ent9.place(x= 300, y= 460)
    ent10.place(x= 300, y= 480)
    ent11.place(x= 300, y= 500)
    ent12.place(x= 300, y= 520)
    ent13.place(x= 300, y= 540)
    ent14.place(x= 300, y= 560)
    
    
    #make third button
    btn3=Button(
    win,
    text="Submit", 
    command=printValue,
    activeforeground='blue'
    ).place(x= 350, y= 580)

#make second button   
btn2=Button(
    win,
    text="Enter information about your system",
    width=40, height=5,
    command=func2,
    activeforeground='blue'
    ).place(x= 100, y= 100)


win.mainloop() #running the loop that works as a trigger

