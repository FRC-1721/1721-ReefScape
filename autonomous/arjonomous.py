import wpilib
from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve

# quick template for making autos


class ArjAuto(AutonomousStateMachine):

    MODE_NAME = "ArjAuto"
    DEFAULT = True
    DISABLED = False

    swerve: Swerve

    @timed_state(duration=0.5, next_state="armove", first = True)
    def arwait(self, tm, initial_call):
        pass

    @state()
    def armove(self, tm, initial_call):
        self.swerve.go(0.1, 0, 0, False)