clc
clear all
close all

% filename = '../gravity_polar.txt';
filename = '../experiments/17_11_17__10_01';

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

% Subtract gravity polar if it is not that measurement
load('grav_calibration.mat')

R_cal = bsxfun(@minus,R(:,1:6), [ones(length(R),1) sin(arm_pos) cos(arm_pos)]*model_fit);

C40 =  [ 0.10573,  -0.04946,  -0.03339,   6.31374,  -0.04072,  -6.35659 ;
		 0.24983,  -7.21789,   0.12016,   3.62807,  -0.08762,   3.70953 ;
		10.12504,   0.21548,  10.10169,   0.36926,  10.57529,   0.28278 ;
		-0.00249,  -0.03763,   0.14501,   0.02394,  -0.15264,   0.01486 ;
		-0.17046,  -0.00215,   0.08486,  -0.03049,   0.08772,   0.03596 ;
		 0.00226,  -0.08472,  -0.00019,  -0.08519,   0.00105,  -0.08698 ];

% R_cal = bsxfun(@minus,R(:,1:6),B40);
limit_check = C40*(R(:,1:6).');
limit_check = limit_check.';
R_cal = C40*R_cal.';
R_cal = R_cal.';

figure; plot(R_cal(:,1:3)); title('forces')
figure; plot(R_cal(:,4:6)); title('moments')

% Rough airspeed
airspeed = sqrt(R(:,7) - .545) / 0.0620;