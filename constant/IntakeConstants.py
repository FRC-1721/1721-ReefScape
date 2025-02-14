import util

import wpimath.controller
import phoenix6


PosMotorID = 0
PosMotorClass = phoenix6.hardware.talon_fx.TalonFX

IntakeMotorID = 0
IntakeMotorClass = phoenix6.hardware.talon_fx.TalonFX

# haha im so silly
Controller = wpimath.controller.PIDController(
    *(
        PID := [
            P := 1,
            I := 0,
            D := 0,
        ]
    )
)

FFController = wpimath.controller.ArmFeedforward(
    *(
        FF := [  # FeedForward
            kS := 0,  # Static friction feedforward
            kG := 0,
            kV := 0,  # Velocity feedforward
            kA := 0,  # Acceleration feedforward
        ]
    )
)

clamp = util.clamp(0.5, -0.5)

# In Out positions
PosIn = 0
PosOut = 0

# Intake/Eject speeds
IntakeIntake = 0.5
IntakeEject = -0.2
