pybot_arm is a high-level Python package created to solve the robot arm 
benchmark optimal control problem. The goal of this problem is to determine 
the set of controls that minimize the time taken for a robot arm to complete 
a user-specified manuever in minimal time. The user is able to change the 
parameters of the problem and solve for the corresponding optimal 
trajectory/controls. Users can either use the modules and corresponding 
methods directly (as shown below) or use the provided GUI.

To use modules directly: import pybot_arm.pybot_ocp, pybot_arm.pybot_plot

To use GUI from shell/terminal: python runGUI.py

Consider the following optimal control problem:
min π‘π 

subject to the following dynamic constraints

πΏπΒ¨=π’π, πΌππΒ¨=π’π, πΌππΒ¨=π’π ,

state bounds

π(π‘)β[0,πΏ], |π(π‘)|β€π, 0β€π(π‘)β€π ,

control bounds

|π’π|β€1, |π’π|β€1, |π’π|β€1 ,

and boundary conditions

(π(0),π(π‘π))=(π0,ππ)       (π(0),π(π‘π))=(π0,ππ)       (π(0),π(π‘π))=(π0,ππ)    
(πΛ(0),πΛ(π‘π))=(πΛ0,πΛπ)   (πΛ(0),πΛ(π‘π))=(πΛ0,πΛπ)   (πΛ(0),πΛ(π‘π))=(πΛ0,πΛπ)

Reference: Dolan, Elizabeth D., Jorge J. MorΓ©, and Todd S. Munson. 
Benchmarking optimization software with COPS 3.0. No. ANL/MCS-TM-273. 
Argonne National Lab., Argonne, IL (US), 2004. 
(https://www.mcs.anl.gov/~tmunson/papers/cops.pdf)


Modules/functions:

-pybot_ocp

pybot_ocp.solve_pybot 
Function to create casADI Opti stack object for the robot arm OCP.

    Parameters
    ----------
    N : int
        Number of control intervals.
    L : float
        Length of robot arm.
    bounds : dict
        Dictionary of boundary conditions [z0,zf] for 
        keys "rho","rho_dot","theta","theta_dot","phi","phi_dot"

    Returns
    -------
    (solve_ocp,info) : tuple 
        Robot arm OCP solution. 
        Tuple consists of (casadi.OptiSol object, dict of problem vars/constants)

pybot_ocp.export_to_csv
Export solution to CSV file for post-processing.

    Parameters
    ----------
    sol : tuple 
        Robot arm OCP solution. 
        Tuple consists of (casadi.OptiSol object, dict of problem vars/constants)
    filename : str
        Desired CSV filename (without .csv).
    path : str, optional
        Desired path for file location. The default is str(Path.cwd()).

    Returns
    -------
    None.

pybot_ocp.parse_sol
Extract solution components from OptiSol object

    Parameters
    ----------
    sol : tuple 
        Robot arm OCP solution. 
        Tuple consists of (casadi.OptiSol object, dict of problem vars/constants)

    Returns
    -------
    time : np.ndarray
        Array of discrete time points.
    X : np.ndarray
        2D array of state variables at each time point.
    U : np.ndarray
        2D array of control variables at each time point.

-pybot_plot

pybot_plot.read_csv_data
    This function reads the csv file and converts the data from spherical 
    coordinates to Cartesian coordinates. It returns the position, velocity, 
    and acceleration in Cartesian coordinates along with the control output in
    spherical coordinates.
    
        Parameters
    ----------
    csv_file : string
        the .csv file containing the solution data

    Returns
    -------
    (position, velocity, acceleration, control, time) : lists
        the position, velocity, and acceleration in Cartesian coordinates
        along with the spherical coordinate control output and time

pybot_plot.create_plots
    This function creates 3 subplots vs time with labels and a titles. 
    Specifying plot_type control will use rho, theta, phi coordinates
    
    Parameters
    ----------
    data: list
    the position, velocity, acceleration, or control data output from
    the read_csv_data function
    
    plot_type: str (position, velocity, acceleration, control)
       Choosing the type will adjust the axis labels and titles of the plot.
       Specifying plot_type of  position, velocity, or acceleration will use 
       x, y, z coordinates while control will use spherical coordinates. 
       Specifying position will also output a 3D plot of the trajectory.

    Returns
    -------
    None.

pybot_plot.animate_3D

    This function creates 3D animation given the x, y, and z data of the trajectory. 
    
    Parameters
    ----------
    position : list
        the position output from the read_csv_data function 
        
    Returns
    -------
    animate : matplotlib.animation.FuncAnimation
        a 3D animation of the position trajectory in Cartesian coordinates


-GUI 

runGUI.func1
    
    This function displays a welcome message to the user and prompts them to enter information about their system.
    
    Parameters
    ----------
    none 
        
    Returns
    -------
    none
    
runGUI.func2
    
    This function gets entries from user for number of points, length of robot arm, and the intitial and final values
    for rho, theta, phi, rho_dot, theta_dot and phi_dot. It will display an error if the entered values are outside of
    the acceptable range
    
    Parameters
    ----------
    none 
        
    Returns
    -------
    none
    
runGUI.func4

    This function takes the user's entries and uses pybot_ocp.solve_pybot and pybot_ocp.export_to_csv to perform calculations and 
    export the solution to a csv file.
    
    Parameters
    ----------
    none 
        
    Returns
    -------
    none
