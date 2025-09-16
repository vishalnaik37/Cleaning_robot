import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/root/freefleet_ws/UR5_AMR_CL_4/install/robotic_arms_control'
