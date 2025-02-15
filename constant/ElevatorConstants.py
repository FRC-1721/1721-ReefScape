import wpimath.controller
import phoenix6
import util


Motor1ID = 14
Motor2ID = 15
EncoderID = 16

MotorClass = phoenix6.hardware.talon_fx.TalonFX

# CAN Bus
# TODO: Change to "can of war" lol
Motor1Canbus = "rio"
Motor2Canbus = "rio"
EncoderCanbus = "rio"

up = 0.5
stay = 0.025
down = 0.002

dampen = 0.5
clamp = util.clamp(0.4, -0.1)

config = phoenix6.configs.TalonFXConfiguration()
config.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE
config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE

Controller = wpimath.controller.PIDController(
    *(
        PID := [
            P := 0.035,
            I := 0.01,
            D := 0.000,
        ]
    )
)

FFController = wpimath.controller.ElevatorFeedforward(  # Feedforward
    *(
        FF := [
            kS := 0.00,  # Static friction feedforward
            kG := 0.022,
            kV := 0.00,  # Velocity feedforward
            kA := 0.000,  # Acceleration feedforward
        ]
    )
)


class Setpoint:
    MIN_HEIGHT = 0.0  # Minimum Height
    LAURA = 76.8  # Maximum Height

    HOME = 7
    SRC = 0
    TROUGH = 0
    L1 = 15
    L2 = 35
    L3 = 0
