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
    # goal_pos = Const.PosIn
    eject_dampen = will_reset_to(Const.IntakeDampen)
    goal_pos = will_reset_to(0)
    controller = Const.Controller
    feed_forward = Const.FFController

    def intake(self):
        self.intaking = True

    def eject(self, dampen=Const.IntakeDampen):
        self.intaking = False
        self.eject_dampen = dampen

    def set(self, setpoint):
        self.goal_pos = setpoint

    def isReady(self, desiredPOS):
        if round(self.posMotor.get_position()) == desiredPOS:
            return True

    def execute(self):
        if self.intaking is not None:
            if self.intaking:
                self.intakeMotor.set(Const.IntakeIntake)
            else:
                self.intakeMotor.set(Const.IntakeEject * self.eject_dampen)
        else:
            self.intakeMotor.set(0)

        # self.posMotor.set(Const.clamp(self.goal_pos * Const.PosDampen))
        current_position = self.posMotor.get_position().value
        pid_output = self.controller.calculate(current_position, self.goal_pos)
        self.posMotor.set(Const.clamp(pid_output))
