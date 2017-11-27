
dt = diff(time);

index = find(dt>1);

index = [0; index; length(arm_pos)];

for i=1:length(index)-1
    index_mean(i) = mean([index(i),index(i+1)]);
    time_mean(i) = time(round(index_mean(i)));
    arm_mean(i) = mean(arm_pos(index(i)+1:index(i+1)));
    
    R_mean(i,:) = mean(R(index(i)+1:index(i+1),1:6),1);
end

R_grav = R_mean; arm_grav = arm_mean.';

offset = ones(length(arm_grav),1);
inputs = [offset sin(arm_grav) cos(arm_grav)];
model_fit = inputs\R_grav;


save('grav_calibration', 'model_fit')