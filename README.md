
pybot_arm is a high-level Python package created to solve the robot arm 
benchmark optimal control problem. The goal of this problem is to determine 
the set of controls that minimize the time taken for a robot arm to complete 
a user-specified manuever in minimal time. The user is able to change the 
parameters of the problem and solve for the corresponding optimal 
trajectory/controls. Users can either use the modules and corresponding 
methods directly (as shown below) or use the provided GUI.


Consider the following optimal control problem:
min 𝑡𝑓 

subject to the following dynamic constraints

𝐿𝜌¨=𝑢𝜌, 𝐼𝜃𝜃¨=𝑢𝜃, 𝐼𝜙𝜙¨=𝑢𝜙 ,

state bounds

𝜌(𝑡)∈[0,𝐿], |𝜃(𝑡)|≤𝜋, 0≤𝜙(𝑡)≤𝜋 ,

control bounds

|𝑢𝜌|≤1, |𝑢𝜃|≤1, |𝑢𝜙|≤1 ,

and boundary conditions

(𝜌(0),𝜌(𝑡𝑓))=(𝜌0,𝜌𝑓)       (𝜃(0),𝜃(𝑡𝑓))=(𝜃0,𝜃𝑓)       (𝜙(0),𝜙(𝑡𝑓))=(𝜙0,𝜙𝑓)    
(𝜌˙(0),𝜌˙(𝑡𝑓))=(𝜌˙0,𝜌˙𝑓)   (𝜃˙(0),𝜃˙(𝑡𝑓))=(𝜃˙0,𝜃˙𝑓)   (𝜙˙(0),𝜙˙(𝑡𝑓))=(𝜙˙0,𝜙˙𝑓)

Reference: Dolan, Elizabeth D., Jorge J. Moré, and Todd S. Munson. 
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
    Specyfing plot_type control will use rho, theta, phi coordinates
    
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

