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
    x = will_reset_to(0)
    controller = Const.Controller
    feed_forward = Const.FFController

    def __init__(self):
        # custom position move controller
        self.moving = False
        self.goal_pos = 0
        self.pos_frames = 0
        self.pos_negative = False

    def intake(self):
        self.intaking = True

    def eject(self, dampen=Const.IntakeDampen):
        self.intaking = False
        self.eject_dampen = dampen

    def set(self, value):
        self.moving = False
        self.x = value

    def goal(self, setpoint):
        self.moving = True
        self.goal_pos = setpoint
        self.pos_frames = 0
        self.pos_negative = self.goal_pos < self.pos()

    def execute(self):
        if self.intaking is not None:
            if self.intaking:
                self.intakeMotor.set(Const.IntakeIntake)
            else:
                self.intakeMotor.set(Const.IntakeEject * self.eject_dampen)
        else:
            self.intakeMotor.set(0)

        # # Hard limit on PosOut
        # if self.pos() < Const.PosOut:
        #     self.posMotor.set((Const.PosOut - self.pos()) * 0.3)

        # custom position move controller
        # if self.moving:
        #     distance = self.goal_pos - self.pos()
        #     self.posMotor.set(
        #         Const.PosDampen
        #         * (-1 if self.pos_negative else 1)
        #         * min(self.pos_frames / Const.PosRampFramesNumber, 1)  # initial ramp
        #         * min(abs(distance) / Const.PosRampFramesNumber, 1)  # final ramp
        #         + 0.3 * math.sin((util.clamp(0, 60)(-self.pos()) * math.pi) / 60)
        #     )
        #     self.pos_frames += 1
        #     if distance * (-1 if self.pos_negative else 1) < Const.PosGoalThreshhold:
        #         self.moving = False
        # else:
        #     self.posMotor.set(self.x)

    @feedback
    def pos(self) -> float:
        return self.posMotor.get_position().value
