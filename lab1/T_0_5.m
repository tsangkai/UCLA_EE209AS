function y = T_0_5(t_vec)
   t1 = t_vec(1);
   t2 = t_vec(2);
   t3 = t_vec(3);
   t4 = t_vec(4);
   
   y = T_0_1(t1) * T_1_2(t2) * T_2_3(t3) * T_3_4(t4) * T_4_5();
end

% data source:
% http://www.theergonomicscenter.com/graphics/Workstation%20Design/Tables.pdf