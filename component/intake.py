import math

import util
import constant.IntakeConstants as Const

from wpimath.controller import PIDController
from magicbot import feedback, will_reset_to


class Intake:
    """
    Robot Intake Component
    """

    # Hardware
    posMotor: Const.PosMotorClass
    intakeMotor: Const.IntakeMotorClass

    intaking = will_reset_to(None)
    eject_dampen = will_reset_to(Const.IntakeDampen)

    def __init__(self):
        self.x = 0

    def intake(self):
        self.intaking = True

    def eject(self, dampen=Const.IntakeDampen):
        self.intaking = False
        self.eject_dampen = dampen

    def set(self, value):
        self.moving = False
        self.x = value

    def execute(self):
        if self.intaking is not None:
            if self.intaking:
                self.intakeMotor.set(Const.IntakeIntake)
            else:
                self.intakeMotor.set(Const.IntakeEject * self.eject_dampen)
        else:
            self.intakeMotor.set(0)

        self.posMotor.set_control(Const.PIDControl(self.x))

    @feedback
    def pos(self) -> float:
        return self.posMotor.get_position().value
