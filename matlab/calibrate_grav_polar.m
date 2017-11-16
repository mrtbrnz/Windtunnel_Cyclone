
dt = diff(time);

index = find(dt>1);

index = [0; index; length(arm_pos)];

for i=1:length(index)-1
    index_mean(i) = mean([index(i),index(i+1)]);
    time_mean(i) = time(round(index_mean(i)));
    arm_mean(i) = mean(arm_pos(index(i)+1:index(i+1)));
    
    R_mean(i,:) = mean(R_cal(index(i)+1:index(i+1),:),1);
end

R_grav = R_mean; arm_grav = arm_mean;

save('grav_calibration', 'R_grav', 'arm_grav')