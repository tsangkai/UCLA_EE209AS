
% parameters
threshold = 0.1;

% state specification

final_state = [5 -5 8 1]';
now_state = [0 0 -36.88-35.92 1]';




% start
err = ms_error(final_state, now_state);
action = [pi pi*1.5 0 pi*1.5]';

data = [now_state'];
err_data = [err];

while err > threshold
    delta = final_state(1:3) - now_state(1:3);
    
    action = action + pinv(Jacob(action)) * delta;
    
    now_state = T_0_5(action) * [0 0 0 1]';
    err = ms_error(final_state, now_state);
    
    data = [data; now_state'];
    err_data = [err_data; err]
    
    pause
    
end


