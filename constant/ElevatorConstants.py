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

    # PID Constants
    class LiftPID:
        P = 0.025
        I = 0.00001
        D = 3.7
        F = 0.0

    # Feedforward Constants
    class LiftFF:
        kS = 0.2  # Static friction feedforward
        kV = 0.1  # Velocity feedforward
        kA = 0.01  # Acceleration feedforward


class Setpoints:
    MIN_HEIGHT = 0.0  # Minimum Height
    LAURA = 100.0  # Maximum Height
