import phoenix6


class Constants:
    # Motor IDs
    Motor1ID = 14
    Motor2ID = 15
    EncoderID = 16

    # CAN Bus
    # TODO: Change to "can of war" lol
    Motor1Canbus = "rio"
    Motor2Canbus = "rio"
    EncoderCanbus = "rio"

    dampen = 0.1

    up = 0.5
    stay = 0.024
    down = -0.1

    config = phoenix6.configs.TalonFXConfiguration()
    config.motor_output.inverted = phoenix6.signals.InvertedValue.CLOCKWISE_POSITIVE
    config.motor_output.neutral_mode = phoenix6.signals.NeutralModeValue.BRAKE

    # PID Constants
    class LiftPID:
        P = 0.025
        # I = 0.00001
        # D = 3.7
        I = 0.02
        D = 0.000
        F = 0.0

    # Feedforward Constants
    class LiftFF:
        kS = 0.00  # Static friction feedforward
        kG = 0.001
        kV = 0.00  # Velocity feedforward
        kA = 0.000  # Acceleration feedforward


class Setpoints:
    MIN_HEIGHT = 0.0  # Minimum Height
    LAURA = 76.8  # Maximum Height

    HOME = 5
    LOW = 10
    HIGH = 35
