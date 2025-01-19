from phoenix6 import CANBus, configs, hardware, signals, swerve, units
from wpimath.units import inchesToMeters, rotationsToRadians

"""
Generated by the Tuner X Swerve Project Generator
https://v6.docs.ctr-electronics.com/en/stable/docs/tuner/tuner-swerve/index.html
"""

# Both sets of gains need to be tuned to your individual robot

# The steer motor uses any SwerveModule.SteerRequestType control request with the
# output type specified by SwerveModuleConstants.SteerMotorClosedLoopOutput
_steer_gains = (
    configs.Slot0Configs()
    .with_k_p(100)
    .with_k_i(0)
    .with_k_d(0.5)
    .with_k_s(0.1)
    .with_k_v(3.1)
    .with_k_a(0)
    .with_static_feedforward_sign(
        signals.StaticFeedforwardSignValue.USE_CLOSED_LOOP_SIGN
    )
)
# When using closed-loop control, the drive motor uses the control
# output type specified by SwerveModuleConstants.DriveMotorClosedLoopOutput
_drive_gains = (
    configs.Slot0Configs()
    .with_k_p(0.1)
    .with_k_i(0)
    .with_k_d(0)
    .with_k_s(0)
    .with_k_v(0.124)
)

# The closed-loop output type to use for the steer motors;
# This affects the PID/FF gains for the steer motors
_steer_closed_loop_output = swerve.ClosedLoopOutputType.VOLTAGE
# The closed-loop output type to use for the drive motors;
# This affects the PID/FF gains for the drive motors
_drive_closed_loop_output = swerve.ClosedLoopOutputType.VOLTAGE

# The type of motor used for the drive motor
_drive_motor_type = swerve.DriveMotorArrangement.TALON_FX_INTEGRATED
# The type of motor used for the drive motor
_steer_motor_type = swerve.SteerMotorArrangement.TALON_FX_INTEGRATED

_drive_motor_class = hardware.TalonFX
_steer_motor_class = hardware.TalonFX
_encoder_class = hardware.CANcoder

# The remote sensor feedback type to use for the steer motors;
# When not Pro-licensed, FusedCANcoder/SyncCANcoder automatically fall back to RemoteCANcoder
_steer_feedback_type = swerve.SteerFeedbackType.FUSED_CANCODER

# The stator current at which the wheels start to slip;
# This needs to be tuned to your individual robot
_slip_current: units.ampere = 120.0

# Initial configs for the drive and steer motors and the azimuth encoder; these cannot be null.
# Some configs will be overwritten; check the `with_*_initial_configs()` API documentation.
_drive_initial_configs = configs.TalonFXConfiguration()
_steer_initial_configs = configs.TalonFXConfiguration().with_current_limits(
    configs.CurrentLimitsConfigs()
    # Swerve azimuth does not require much torque output, so we can set a relatively low
    # stator current limit to help avoid brownouts without impacting performance.
    .with_stator_current_limit(60).with_stator_current_limit_enable(True)
)
_encoder_initial_configs = configs.CANcoderConfiguration()
# Configs for the Pigeon 2; leave this None to skip applying Pigeon 2 configs
_pigeon_configs: configs.Pigeon2Configuration | None = None

# CAN bus that the devices are located on;
# All swerve devices must share the same CAN bus
canbus = CANBus("", "./logs/example.hoot")

# Theoretical free speed (m/s) at 12 V applied output;
# This needs to be tuned to your individual robot
speed_at_12_volts: units.meters_per_second = 5.12

# Every 1 rotation of the azimuth results in _couple_ratio drive motor turns;
# This may need to be tuned to your individual robot
_couple_ratio = 0

_drive_gear_ratio = 6.23
_steer_gear_ratio = 25
_wheel_radius: units.meter = inchesToMeters(2)

_invert_left_side = False
_invert_right_side = True

_pigeon_id = 1

# These are only used for simulation
_steer_inertia: units.kilogram_square_meter = 0.01
_drive_inertia: units.kilogram_square_meter = 0.01
# Simulated voltage necessary to overcome friction
_steer_friction_voltage: units.volt = 0.2
_drive_friction_voltage: units.volt = 0.2

drivetrain_constants = (
    swerve.SwerveDrivetrainConstants()
    .with_can_bus_name(canbus.name)
    .with_pigeon2_id(_pigeon_id)
    .with_pigeon2_configs(_pigeon_configs)
)

_constants_creator: swerve.SwerveModuleConstantsFactory[
    configs.TalonFXConfiguration,
    configs.TalonFXConfiguration,
    configs.CANcoderConfiguration,
] = (
    swerve.SwerveModuleConstantsFactory()
    .with_drive_motor_gear_ratio(_drive_gear_ratio)
    .with_steer_motor_gear_ratio(_steer_gear_ratio)
    .with_coupling_gear_ratio(_couple_ratio)
    .with_wheel_radius(_wheel_radius)
    .with_steer_motor_gains(_steer_gains)
    .with_drive_motor_gains(_drive_gains)
    .with_steer_motor_closed_loop_output(_steer_closed_loop_output)
    .with_drive_motor_closed_loop_output(_drive_closed_loop_output)
    .with_slip_current(_slip_current)
    .with_speed_at12_volts(speed_at_12_volts)
    .with_drive_motor_type(_drive_motor_type)
    .with_steer_motor_type(_steer_motor_type)
    .with_feedback_source(_steer_feedback_type)
    .with_drive_motor_initial_configs(_drive_initial_configs)
    .with_steer_motor_initial_configs(_steer_initial_configs)
    .with_encoder_initial_configs(_encoder_initial_configs)
    .with_steer_inertia(_steer_inertia)
    .with_drive_inertia(_drive_inertia)
    .with_steer_friction_voltage(_steer_friction_voltage)
    .with_drive_friction_voltage(_drive_friction_voltage)
)

front_left = _constants_creator.create_module_constants(
    28,  # front_left.drive_motor_id
    1,  # front_left.steer_motor_id
    13,  # front_left.encoder_id
    -0.417724609375,  # front_left.encoder_offset: units.rotation
    inchesToMeters(11.75),  # front_left.location_x: units.meter
    inchesToMeters(11.75),  # front_left.location_y: units.meter
    _invert_left_side,  # front_left.drive_motor_inverted
    False,  # front_left.steer_motor_inverted
    False,  # front_left.encoder_inverted
)
front_right = _constants_creator.create_module_constants(
    3,  # front_right.drive_motor_id
    5,  # front_right.steer_motor_id
    41,  # front_right.encoder_id
    -0.197998046875,  # front_right.encoder_offset: units.rotation
    inchesToMeters(11.75),  # front_right.location_x: units.meter
    inchesToMeters(-11.75),  # front_right.location_y: units.meter
    _invert_right_side,  # front_right.drive_motor_inverted
    False,  # front_right.steer_motor_inverted
    False,  # front_right.encoder_inverted
)
back_left = _constants_creator.create_module_constants(
    12,  # back_left.drive_motor_id
    62,  # back_left.steer_motor_id
    40,  # back_left.encoder_id
    -0.393310546875,  # back_left.encoder_offset: units.rotation
    inchesToMeters(-11.75),  # back_left.location_x: units.meter
    inchesToMeters(11.75),  # back_left.location_y: units.meter
    _invert_left_side,  # back_left.drive_motor_inverted
    False,  # back_left.steer_motor_inverted
    False,  # back_left.encoder_inverted
)
back_right = _constants_creator.create_module_constants(
    2,  # back_right.drive_motor_id
    8,  # back_right.steer_motor_id
    9,  # back_right.encoder_id
    -0.1513671875,  # back_right.encoder_offset: units.rotation
    inchesToMeters(-11.75),  # back_right.location_x: units.meter
    inchesToMeters(-11.75),  # back_right.location_y: units.meter
    _invert_right_side,  # back_right.drive_motor_inverted
    False,  # back_right.steer_motor_inverted
    False,  # back_right.encoder_inverted
)

modules = (
    front_left,
    front_right,
    back_left,
    back_right,
)


def get_drive_motors():
    return tuple(map(lambda x: _drive_motor_class(x.drive_motor_id), modules))


def get_steer_motors():
    return tuple(map(lambda x: _steer_motor_class(x.steer_motor_id), modules))


def get_motors():
    return get_drive_motors() + get_steer_motors()
