import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import pandas as pd



##############################################################################

def read_csv_data(csv_file):
    """
    This function reads the csv file and converts the data from spherical 
    coordinates to Cartesian coordinates. It returns the position, velocity, 
    and acceleration in Cartesian coordinates along with the control output in
    spherical coordinates.
    """
    
    df = pd.read_csv(csv_file)
    # time
    time = df.time
    
    # spherical robot arm controls
    u_rho = df.u_rho 
    u_theta = df.u_theta
    u_phi = df.u_phi
    control = [u_rho, u_theta, u_phi]
    
    #converting from sperical to cartesian coordinates
    x = df.rho * np.sin(df.phi) * np.cos(df.theta)
    y = df.rho * np.sin(df.phi) * np.sin(df.theta)
    z = df.rho * np.cos(df.phi)
    position = [x, y, z]
    
    x_dot = df.rho_dot * np.sin(df.phi_dot) * np.cos(df.theta_dot)
    y_dot = df.rho_dot * np.sin(df.phi_dot) * np.sin(df.theta_dot)
    z_dot = df.rho_dot * np.cos(df.phi_dot)
    velocity = [x_dot, y_dot, z_dot]
    
    x_ddot = df.rho_ddot * np.sin(df.phi_ddot) * np.cos(df.theta_ddot)
    y_ddot = df.rho_ddot * np.sin(df.phi_ddot) * np.sin(df.theta_ddot)
    z_ddot = df.rho_ddot * np.cos(df.phi_ddot)
    acceleration = [x_ddot, y_ddot, z_ddot]
    
    return (position, velocity, acceleration, control, time)
    
    

##############################################################################

def create_plots( data, time, plot_type):
    
     
    """
    This function creates 3 subplots vs time with labels and a titles. 
    
    data: the position, velocity, acceleration, or control data output from
    the read_csv_data function
    
     
    plot_type: position, velocity, acceleration, control
       Choosing the type will adjust the axis labels and titles of the plot.
       Specifying plot_type of  position, velocity, or acceleration will use 
       x, y, z coordinates.
       Specyfing plot_type control will use rho, theta, phi coordinates
    """
    

    
    plot_type = plot_type.strip()
    plot_type = plot_type.lower()
    
    if plot_type == 'control':
        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(8, 8))
        fig.tight_layout(pad=3)
        ax1.plot(data[0], time)
        ax2.plot(data[1], time)
        ax3.plot(data[2],time)
        fig.suptitle('Control vs Time')
        ax1.set_title('rho-control vs time')
        ax2.set_title('theta-control vs time')
        ax3.set_title('phi-control vs time')
        
    elif plot_type == 'position':
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        plt.title('Position vs Time')
        plt.plot(position[0], position[1], position[2])
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(8, 8))
        fig.tight_layout(pad=3)
        ax1.plot(data[0], time)
        ax2.plot(data[1], time)
        ax3.plot(data[2],time)
        fig.suptitle('Position vs Time')
        ax1.set_title('x-position vs Time')
        ax2.set_title('y-position vs Time')
        ax3.set_title('z-position vs Time')
        
        
    
    elif plot_type == 'velocity' or plot_type == 'acceleration':
        fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(8, 8))
        fig.tight_layout(pad=3)
        ax1.plot(data[0], time)
        ax2.plot(data[1], time)
        ax3.plot(data[2],time)
        fig.suptitle(f'{plot_type.capitalize()} vs Time')
        ax1.set_title(f'x-{plot_type} vs Time')
        ax2.set_title(f'y-{plot_type} vs Time')
        ax3.set_title(f'z-{plot_type} vs Time')
       
    else:
        raise ValueError('plot_type must be position, velocity, acceleration, or control')
            

##############################################################################

def animate_3D(position):
    """
    This function creates 3D animation given the x, y, and z data of the trajectory. 
    
    """
    
    def func(num, dataSet, line):
        line.set_data(dataSet[0:2, :num])
        line.set_3d_properties(dataSet[2, :num])
        
    #dataSet = np.array([x, y, z])
    #dataSet = position
    numDataPoints = len(position[0])
    
    fig = plt.figure()
    ax = Axes3D(fig)
    #line =plt.plot(dataSet[0], dataSet[1], dataSet[2], lw=2, c='g')[0]
    line = plt.plot(position[0], position[1], position[2], lw=2, c='g')[0]
    ax.set_xlabel('X(t)')
    ax.set_ylabel('Y(t)')
    ax.set_zlabel('Z(t)')
    
    line_ani = animation.FuncAnimation(fig, func, frames=numDataPoints, fargs=(position, line))
    plt.show()

##############################################################################