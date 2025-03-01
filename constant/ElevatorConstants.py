import wpimath.controller
from wpilib import DigitalInput
import phoenix6
import util


Motor1ID = 14
Motor2ID = 15
LimitID = 0

MotorClass = phoenix6.hardware.talon_fx.TalonFX
LimitClass = DigitalInput

# CAN Bus
Motor1Canbus = "intakebus"
Motor2Canbus = "intakebus"

up = 0.5
stay = 0.025
down = 0.002

deadzone = util.deadzone(0.05)
dampen = 1
clamp = util.clamp(0.4, -0.3)

config = phoenix6.configs.TalonFXConfiguration()
config.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE
config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE

Controller = wpimath.controller.PIDController(
    *(
        PID := [
            P := 0.050,
            I := 0.000,
            D := 0.010,
        ]
    )
)

FFController = wpimath.controller.ElevatorFeedforward(  # Feedforward
    *(
        FF := [
            kS := 0.00,  # Static friction feedforward
            kG := 0.001,
            kV := 0.00,  # Velocity feedforward
            kA := 0.000,  # Acceleration feedforward
        ]
    )
)


class Setpoint:
    MIN_HEIGHT = 0.0  # Minimum Height
    LAURA = 76.8  # Maximum Height

    HOME = 0
    SRC = 0
    TROUGH = 0
    L1 = 17
    L2 = 40
    L3 = 0
