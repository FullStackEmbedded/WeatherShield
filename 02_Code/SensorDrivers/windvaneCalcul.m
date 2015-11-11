
clc 
Rx   = [ 33, 6.57, 8.2, 0.891, 1, 0.688, 2.2, 1.41, 3.9, 3.14, 16, 14.12, 120, 42.12, 64.9, 21.88];
Uges = 3.3;
R1   = 20;

vout = (Rx .*Uges)./(Rx + R1)
fprintf("min_val = %f\n",min(vout))
fprintf("max_val = %f\n",max(vout))
