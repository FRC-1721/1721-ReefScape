import wpilib
import logging
import ntcore

from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve
from component.intake import Intake

from constant import IntakeConstants

# quick template for making autos


class StraightAuto(AutonomousStateMachine):

    MODE_NAME = "Go Straight"
    DEFAULT = False
    DISABLED = False

    # Components
    swerve: Swerve
    intake: Intake

    @timed_state(duration=0.5, next_state="armove", first=True)
    def arwait(self):
        self.startx = self.swerve.pose()[0]
        logging.debug(f"ArjAuto set startx to {self.startx}")

    @state()
    def armove(self, initial_call):
        distance_driven = self.swerve.pose()[0] - self.startx

        if distance_driven < 2.3:
            self.swerve.go(0.7, 0, 0, False)
        else:
            self.next_state("arout")

    @state()
    def arout(self):
        self.intake.set(4.6)
        self.next_state("ardone")

    @state()
    def ardone(self):
        self.swerve.brake()
