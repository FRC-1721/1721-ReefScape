import wpimath
import phoenix6

import util
import constant.ClimberConstants as Const

from magicbot import feedback, will_reset_to


class Climber:
    climbMotor: Const.MotorClass
    is_climbing = will_reset_to(None)

    def __init__(self):
        self.is_climbing = False
        self.ratchet_engaged = True
        self.timer = 10

    def climb(self):
        self.is_climbing = True

    def unclimb(self):
        self.is_climbing = False

    def execute(self):
        if self.climbing() is not None:
            if self.climbing():
                self.climbMotor.set(Const.ClimbSpeed)
            else:
                self.climbMotor.set(Const.UnclimbSpeed)
        else:
            self.climbMotor.set(0)

    @feedback
    def climbing(self):
        return self.is_climbing
