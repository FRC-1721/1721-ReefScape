import util

import wpimath.controller
import phoenix6


PosMotorClass = phoenix6.hardware.talon_fx.TalonFX
PosMotor = [
    PosMotorID := 31,
    PosMotorCANBus := "intakebus",
]

IntakeMotorClass = phoenix6.hardware.talon_fx.TalonFX
IntakeMotor = [
    IntakeMotorID := 35,
    IntakeMotorCANBus := "intakebus",
]

# haha im so silly
Controller = wpimath.controller.PIDController(
    *(
        PID := [
            P := 0.1,
            I := 0,
            D := 0.05,
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

PosDampen = 0.3
clamp = util.clamp(0.5, -0.5)

# In Out positions
PosIn = 0
PosOut = -46

# Intake/Eject speeds
IntakeIntake = -0.2
IntakeEject = 0.7
IntakeDampen = 1
