# Dallas Formula Racing Aeromap Scripts

Python script to process and visualize aerodynamic performance of the vechicle through different simulations

The main purpose is to create an 'aeromap' which allows us to analysze how the car performs through various rideheights and crosswinds.
The visualized aeromap is a 2d graph where x and y axes are front and rear ride heights respectively, and the z axis is the mean downforce value.

## Java Macros

Uses StarCCM+'s Java api to change input parameters in the CFD simulation. Different versions for sweeping through single variable, 2 variable, and Yaw Angle Cases.

## Python Script

Our simualtions output each iteration as a csv file, so this script merges all iterations together into a single csv file.
Since our input parameters do not have symmetric inputs and currently allign in a line where front and rear ride heights are inversly proportional, we can not use built in methods to plot the data in a heatmap / contour plot. Those require the z axis to be a M * N dimension array where M and N are the lengths of the x and y axes respectively.

Instead we take each iteration in the data frame and copy it n times into a new data frame where n is the rounded downforce value of that iteration, so an interation with a downforce value os 120 will be represented in the new data frame 120 times. This allows us to plot the data as a 2d histogram  with the z axis being the downforce value.
