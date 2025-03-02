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
            P := 0.009,
            I := 0.0005,
            D := 0.002,
        ]
    )
)

FFController = wpimath.controller.ArmFeedforward(
    *(
        FF := [  # FeedForward
            kS := 0,  # Static friction feedforward
            kG := 3,
            kV := 0,  # Velocity feedforward
            kA := 0,  # Acceleration feedforward
        ]
    )
)

PosDampen = 0.3
clamp = util.clamp(0.5, -0.5)

# custom position move controller
PosRampFramesNumber = 10
PosGoalThreshhold = 0.1

# In Out positions
PosHome = -10
PosIn = -5
PosOut = -22

# Intake/Eject speeds
IntakeIntake = -0.2
IntakeEject = 0.3
IntakeDampen = 1
