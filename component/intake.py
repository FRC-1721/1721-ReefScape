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

    algae_intaking = will_reset_to(0)

    def __init__(self):
        self.x = 0

        self.coral_intaking = False

    def intake_coral(self):
        self.coral_intaking = not self.coral_intaking

    def intake_algae(self, slow=False):
        self.algae_intaking = (
            Const.IntakeEjectCoral if slow else Const.IntakeIntakeAlgae
        )

    # for intake position
    def set(self, value):
        self.x = value

    def execute(self):
        if self.algae_intaking:
            self.intakeMotor.set(self.algae_intaking)
        elif self.coral_intaking:
            self.intakeMotor.set(Const.IntakeIntakeCoral)
        else:
            self.intakeMotor.set(0)

        self.posMotor.set_control(Const.PIDControl(self.x))

    @feedback
    def pos(self) -> float:
        return self.posMotor.get_position().value

    @feedback
    def intaking(self) -> float:
        return self.intakeMotor.get_velocity().value
