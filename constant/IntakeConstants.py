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

PIDConfig = phoenix6.configs.Slot0Configs()
PIDConfig.k_p = 1.3621
PIDConfig.k_i = 0.1
PIDConfig.k_d = 0.3

PIDRequest = phoenix6.controls.PositionVoltage(0).with_slot(0).with_feed_forward(0.2)


def PIDControl(x):
    return PIDRequest.with_position(x)


PosDampen = 0.3
clamp = util.clamp(0.5, -0.5)
deadzone = util.deadzone(0.05)

# In Out positions
PosHome = 2
PosIn = 2
PosOut = 22

# Intake/Eject speeds
IntakeIntake = -0.2
IntakeEject = 0.3
IntakeHold = 0.08  # TODO mod to not be guess
