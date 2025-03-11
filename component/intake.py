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
    controller = Const.Controller
    feedforward = Const.FFController

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

        # # Hard limit on PosOut
        # if self.pos() < Const.PosOut:
        #     self.posMotor.set((Const.PosOut - self.pos()) * 0.3)

        current_position = self.pos()

        # pid_output = self.controller.calculate(current_position, self.x)
        # ff_output = self.feedforward.calculate(
        #     current_position,
        #     # (current_position) / 100 * (math.pi * 2),
        #     self.posMotor.get_velocity().value,
        #     # pid_output,
        # )  # Feedforward for motion control
        # ff_output = 0

        # output = pid_output + ff_output
        output = self.controller.calculate(current_position, self.x)
        print(f"current POS:{self.pos()}, current x:{self.x}")
        # Apply PID + FF control
        # print(f"{output} --> {Const.clamp(output)}")
        self.posMotor.set(Const.clamp(output))

    # def execute(self):
    #     if self.intaking is not None:
    #         if self.intaking:
    #             self.intakeMotor.set(Const.IntakeIntake)
    #         else:
    #             self.intakeMotor.set(Const.IntakeEject * self.eject_dampen)
    #     else:
    #         self.intakeMotor.set(0)

    #     # self.posMotor.set(Const.clamp(self.goal_pos * Const.PosDampen))
    #     current_position = self.posMotor.get_position().value
    #     pid_output = self.controller.calculate(current_position, self.goal_pos)
    #     self.posMotor.set(Const.clamp(pid_output))

    @feedback
    def pos(self) -> float:
        return self.posMotor.get_position().value
