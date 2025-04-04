import wpimath.controller
from wpilib import DigitalInput
import phoenix6
import util


MotorClass = phoenix6.hardware.talon_fx.TalonFX
LimitClass = DigitalInput

Motor1 = [
    Motor1ID := 14,
    Motor1Canbus := "intakebus",
]
Motor2 = [
    Motor2ID := 15,
    Motor2Canbus := "intakebus",
]
LimitID = 0

deadzone = util.deadzone(0.05)
dampen = 1
clamp = util.clamp(0.4, -0.3)

config = phoenix6.configs.TalonFXConfiguration()
config.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE
config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE

PIDConfig = phoenix6.configs.Slot0Configs()
PIDConfig.k_p = 1
PIDConfig.k_i = 0.1
PIDConfig.k_d = 0.25

PIDRequest = phoenix6.controls.PositionVoltage(0).with_slot(0).with_feed_forward(0.1)


def PIDControl(x):
    return PIDRequest.with_position(x)


class Setpoint:
    MIN_HEIGHT = 0.0  # Minimum Height
    LAURA = 76.8  # Maximum Height

    HOME = 0
    SRC = 0
    TROUGH = 0
    L1 = 53
    L2 = 37
    L3 = 73.4
