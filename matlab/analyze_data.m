clc
clear all
close all

filename = '../gravity_polar.txt';
% filename = '../v286.txt';

%% Read in Data

M = dlmread(filename);

time = M(:,1);
R(:,1) = M(:,2);
R(:,2) = M(:,3);
R(:,3) = M(:,4);
R(:,4) = M(:,5);
R(:,5) = M(:,6);
R(:,6) = M(:,7);
R(:,7) = M(:,8);
pwm(:,1) = M(:,9);
pwm(:,2) = M(:,10);
pwm(:,3) = M(:,11);
pwm(:,4) = M(:,12);
arm_pos = M(:,13);

time = time - time(1);

B40 = [0.1476432979106903, 0.14606346189975739, -0.11490651965141296, 0.1375323235988617, 0.09234895557165146, -0.29624149203300476];
C40 =  [ 0.10573,  -0.04946,  -0.03339,   6.31374,  -0.04072,  -6.35659 ;
		 0.24983,  -7.21789,   0.12016,   3.62807,  -0.08762,   3.70953 ;
		10.12504,   0.21548,  10.10169,   0.36926,  10.57529,   0.28278 ;
		-0.00249,  -0.03763,   0.14501,   0.02394,  -0.15264,   0.01486 ;
		-0.17046,  -0.00215,   0.08486,  -0.03049,   0.08772,   0.03596 ;
		 0.00226,  -0.08472,  -0.00019,  -0.08519,   0.00105,  -0.08698 ];

R_cal = bsxfun(@plus,R(:,1:6),B40);
R_cal = C40*R_cal.';
R_cal = R_cal.';

if(~strcmp(filename, '../gravity_polar.txt'))
    load('grav_calibration.mat')
end