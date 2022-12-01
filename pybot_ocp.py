#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 15:09:45 2022

@author: gabadia97
"""
import casadi as cas
import numpy as np
import csv
from pathlib import Path

def format_bounds(rho,rho_dot,theta,theta_dot,phi,phi_dot):
    """
    Function to format bounds into an ordered dictionary for setup_pybot.
    
    Parameters
    ----------    
    Each parameter is a list of floats [lb,ub] corresponding to each 
    respective variable.

    Returns
    -------
    bounds : dict
        Dictionary of boundary conditions.

    """
    bounds = {"rho":rho, 
              "rho_dot":rho_dot,
              "theta":theta, 
              "theta_dot":theta_dot,
              "phi":phi, 
              "phi_dot":phi_dot}
    
    return bounds

def pybot_dynamics(x,u,L):
    """
    dx/dt = f(x,u)

    Parameters
    ----------
    x : casadi.MX or numpy.ndarray
        State variables.
    u : casadi.MX or numpy.ndarray
        Control variables.
    L : float
        Length of robot arm.

    Returns
    -------
    dict
        Dictionary of dynamic equations of motion.

    """
    # Parse decision variables
    rho       = x[0]
    rho_dot   = x[1]
    theta     = x[2]
    theta_dot = x[3]
    phi       = x[4]
    phi_dot   = x[5]

    u_rho   = u[0]
    u_theta = u[1]
    u_phi   = u[2]
        
    # Intermediate computations
    I_phi   = ((L-rho)**3 + rho**3) / 3
    I_theta = I_phi * np.sin(phi)**2

    # Dynamic equations of motion for robot arm
    dyn_rho       = rho_dot
    dyn_rho_dot   = u_rho / L
    dyn_theta     = theta_dot
    dyn_theta_dot = u_theta / I_theta
    dyn_phi       = phi_dot
    dyn_phi_dot   = u_phi / I_phi    
        
    return {"rho_dot":dyn_rho,
            "rho_ddot":dyn_rho_dot,
            "theta_dot":dyn_theta,
            "theta_ddot":dyn_theta_dot,
            "phi_dot":dyn_phi,
            "phi_ddot":dyn_phi_dot}

def solve_pybot(N,L,bounds):
    """
    Function to create casADI Opti stack object for the robot arm OCP.

    Parameters
    ----------
    N : int
        Number of control intervals.
    L : float
        Length of robot arm.
    bounds : dict
        Ordered dictionary of boundary conditions [z0,zf] for 
        keys "rho","rho_dot","theta","theta_dot","phi","phi_dot"

    Returns
    -------
    opti : casadi.Opti object
        pybot_arm Opti stack object.

    """
    # Create optimization problem instance
    opti = cas.Opti()
    
    # Define decision variables
    n = 6 # number of state variables
    X = opti.variable(n,N+1) # state trajectory
    rho        = X[0,:]
    rho_dot    = X[1,:]
    theta      = X[2,:]
    theta_dot  = X[3,:]
    phi        = X[4,:]
    phi_dot    = X[5,:]
    
    m = 3 # number of control variables
    U = opti.variable(m,N)   # control trajectory
    u_rho    = U[0,:]
    u_theta  = U[1,:]
    u_phi    = U[2,:]
    
    T = opti.variable()      # final time
    
    # Package variable IDs and problem setup
    info = {"N": N, "L":L, "X":X, "U":U, "T":T}
    
    # Define objective
    opti.minimize(T) # minimize time to perform maneuver
    
    # Define dynamic constraints
    def f(x,u):
        """
        Symbolic representation of dynamic constraints.

        Parameters
        ----------
        x : casadi.MX
            State variables.
        u : casadi.MX
            Control variables.

        Returns
        -------
        casadi.MX
            Symbolic stack of dynamic equations.

        """
        
        dxdt = pybot_dynamics(x, u, L)

        # Return stack of dynamic equations
        return cas.vertcat(dxdt["rho_dot"],
                           dxdt["rho_ddot"],
                           dxdt["theta_dot"],
                           dxdt["theta_ddot"],
                           dxdt["phi_dot"],
                           dxdt["phi_ddot"])
    
    # Perform Runge-Kutta 4 integration of the dynamic constraints
    dt = T/N # length of a control interval
    for k in range(N): # loop over control intervals
        # Runge-Kutta 4 integration
        k1 = f(X[:,k],         U[:,k])
        k2 = f(X[:,k]+dt/2*k1, U[:,k])
        k3 = f(X[:,k]+dt/2*k2, U[:,k])
        k4 = f(X[:,k]+dt*k3,   U[:,k])
        x_next = X[:,k] + dt/6*(k1+2*k2+2*k3+k4) 
        opti.subject_to(X[:,k+1]==x_next) # close the gaps between intervals
    
    # Define path constraints
    opti.subject_to(opti.bounded(0.,rho,L)) # rho: [0,L]
    opti.subject_to(opti.bounded(-cas.pi,theta,cas.pi)) # |theta|<=pi
    opti.subject_to(opti.bounded(0.,phi,cas.pi)) # phi: [0,pi]
    opti.subject_to(opti.bounded(-1.,U,1.)) # |u|<=1
    
    for index,key in enumerate(bounds.keys()):
        # Define boundary conditions
        opti.subject_to(X[index,0] == bounds[key][0])
        opti.subject_to(X[index,-1] == bounds[key][-1])
        
        # Set initial values
        opti.set_initial(X[index,:], bounds[key][0])
    
    # Misc. contraints
    opti.subject_to(T>=0) # Time must be positive
    opti.set_initial(T, 1) # initial guess for final time
    
    # Set numerical solver
    opti.solver("ipopt")
    
    # Solve OCP
    solve_ocp = opti.solve()
    
    # return opti
    return (solve_ocp, info)

def export_to_csv(sol,filename,path=str(Path.cwd())):
    """
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

    """      
    # Extract solution components from OptiSol object
    time, X, X_dot, U = parse_sol(sol)
    
    # Concatenate data
    data = np.vstack([time, X, U,
                      X_dot["rho_ddot"],
                      X_dot["theta_ddot"],
                      X_dot["phi_ddot"]])
    
    # Prepare file location/name and header
    file = path + "/" + filename + ".csv"
    header = ["time",
              "rho","rho_dot","theta","theta_dot","phi","phi_dot",
              "u_rho","u_theta","u_phi","rho_ddot","theta_ddot","phi_ddot"]
    
    # Write to csv file 
    with open(file,"a") as csvfile:               
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data.T)
    
    return None

def parse_sol(sol):
    """
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

    """
    # Parse input
    solve_ocp = sol[0]
    info = sol[1]
    
    # Extract problem size attributes from solution
    n = 6   # number of state variables
    m = 3   # number of control variables
    N = info["N"] # number of intervals
    # N = sol.value_variables()[1].shape[1]   # number of intervals
    
    # Convert casadi MX variable type to float value
    X = solve_ocp.value(info["X"])
    U = solve_ocp.value(info["U"])
    T = solve_ocp.value(info["T"])
    # X = np.reshape(sol.value(sol.opti.x[:n*(N+1)]),(N+1,n)).T
    # U = np.reshape(sol.value(sol.opti.x[n*(N+1):-1]),(N,m)).T
    # T = sol.value(sol.opti.x[-1])
    
    # Convert dimensionless horizon to time array
    dt = T/N                    # compute gap between nodes
    time = np.arange(N+1) * dt  # compute time at each node  
    
    # Compute X_dot
    X_dot = pybot_dynamics(X[:,:N], U[:,:N], info["L"])
    
    # Since control is not computed at final point, pad the array with nan
    pad_U = np.empty((m,1)); pad_U[:] = np.nan
    U = np.append(U,pad_U,axis=1) 
    for key in X_dot.keys():
        X_dot[key] = np.append(X_dot[key],np.nan) # overwrite
    
    return time, X, X_dot, U

def main():
    print(__name__)
    
    N = 100
    
    L = 5
    
    bounds = {"rho": [4.5,4.5],
              "rho_dot": [0,0],
              "theta": [0,2*cas.pi/3],
              "theta_dot": [0,0],
              "phi": [cas.pi/4,cas.pi/4],
              "phi_dot": [0,0]}
    
    sol = solve_pybot(N, L, bounds)
    # sol = solve_pybot(opti)
    export_to_csv(sol,"pybot_L5")
    
    return sol

if __name__ == "__main__":
    sol = main()


    