from constant import TunerConstants

vel_dampen = 0.1
max_vel = TunerConstants.speed_at_12_volts * vel_dampen
vel_deadband = max_vel * 0.02

rot_dampen = 0.5
max_rot = 2 * rot_dampen  # arbitrary value, idk
rot_deadband = max_rot * 0.02
