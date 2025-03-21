import wpimath
import phoenix6

import util
import constant.ClimberConstants as Const

from magicbot import feedback, will_reset_to


class Climber:
    climbMotor: Const.MotorClass
    climbSolenoid: Const.SolenoidClass
    is_climbing = will_reset_to(None)

    def __init__(self):
        self.is_climbing = False
        self.ratchet_engaged = True
        self.timer = 10

    def climb(self):
        self.is_climbing = True

    def unclimb(self):
        self.is_climbing = False

    def ratchet(self):
        self.ratchet_engaged = True
        self.climbSolenoid.set(False)

    def free(self):
        self.ratchet_engaged = False
        self.climbSolenoid.set(True)

    def execute(self):
        if self.climbing() is not None:
            if self.climbing():
                if not self.ratcheted():
                    self.ratchet()
                    self.climbMotor.set(Const.FreeSpeed)
                else:
                    self.climbMotor.set(Const.ClimbSpeed)
            else:
                if self.ratcheted():
                    self.free()
                    self.climbMotor.set(Const.FreeSpeed)
                else:
                    self.climbMotor.set(Const.UnclimbSpeed)
        else:
            self.climbMotor.set(0)
            self.ratchet()

    @feedback
    def climbing(self):
        return self.is_climbing

    @feedback
    def ratcheted(self):
        return self.ratchet_engaged
