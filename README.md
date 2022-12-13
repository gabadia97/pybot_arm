pybot_arm is a Python package created to solve the robot arm benchmark optimal control problem. The goal of this problem is to determine the set of controls that minimize the time taken for a robot arm to complete a user-specified manuever in minimal time.

pybot_arm is a high-level package that utilizes the following Python packages:

casadi: open-source tool for nonlinear optimization and algorithmic differentiation
python-control: toolbox for the analysis and design of feedback control systems
matplotlib

Supplemental packages:

-numpy
-csv
-pathlib


Consider the following optimal control problem:

min 𝑡𝑓 

subject to the following dynamic constraints

𝐿𝜌¨=𝑢𝜌, 𝐼𝜃𝜃¨=𝑢𝜃, 𝐼𝜙𝜙¨=𝑢𝜙 ,

state bounds

𝜌(𝑡)∈[0,𝐿], |𝜃(𝑡)|≤𝜋 ,0≤𝜙(𝑡)≤𝜋 

control bounds

|𝑢𝜌|≤1, |𝑢𝜃|≤1, |𝑢𝜙|≤1 

and boundary conditions

(𝜌(0),𝜌(𝑡𝑓))=(𝜌0,𝜌𝑓)    (𝜃(0),𝜃(𝑡𝑓))=(𝜃0,𝜃𝑓)   (𝜙(0),𝜙(𝑡𝑓))=(𝜙0,𝜙𝑓) 

(𝜌˙(0),𝜌˙(𝑡𝑓))=(𝜌˙0,𝜌˙𝑓)   (𝜃˙(0),𝜃˙(𝑡𝑓))=(𝜃˙0,𝜃˙𝑓)   (𝜙˙(0),𝜙˙(𝑡𝑓))=(𝜙˙0,𝜙˙𝑓)

Reference: Dolan, Elizabeth D., Jorge J. Moré, and Todd S. Munson. 
Benchmarking optimization software with COPS 3.0. No. ANL/MCS-TM-273. 
Argonne National Lab., Argonne, IL (US), 2004. (https://www.mcs.anl.gov/~tmunson/papers/cops.pdf)