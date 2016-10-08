
% parameters
threshold = 0.1;

% state specification

final_state = [-10 5 5 1]';
now_state = [0 0 -40 1]';




% start
err = error(final_state, now_state);
action = [pi pi/2 pi pi/2]';

data = [now_state'];
err_data = [err];

while err > threshold
    delta = final_state(1:3) - now_state(1:3);
    
    % normalized
    %delta = delta ./ norm(delta);
    %delta = delta .* step;
    
    action = action + pinv(Jacob(action)) * delta;
    
    now_state = T_0_5(action) * [0 0 0 1]';
    err = error(final_state, now_state);
    
    data = [data; now_state'];
    err_data = [err_data; err];
    
    %pause
    
end


