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

    motor_speed = will_reset_to(0)

    def __init__(self):
        self.x = 0

    def intake(self, dampen=1):
        self.motor_speed = Const.IntakeIntake * dampen

    def eject(self, dampen=1):
        self.motor_speed = Const.IntakeEject * dampen

    def hold(self, dampen=1):
        self.motor_speed = Const.IntakeHold * dampen

    def set(self, value):
        self.x = value

    def execute(self):
        self.intakeMotor.set(self.motor_speed)
        self.posMotor.set_control(Const.PIDControl(self.x))

    @feedback
    def pos(self) -> float:
        return self.posMotor.get_position().value
