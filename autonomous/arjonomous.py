import wpilib
import logging
import ntcore

from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve
from component.intake import Intake

from constant import IntakeConstants

# quick template for making autos


class ArjAuto(AutonomousStateMachine):

    MODE_NAME = "Arjominous Arjonomous"
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

        if distance_driven < 1.0:
            self.swerve.go(0.25, 0, 0, False)
        else:
            self.next_state("arjout")

    @state()
    def arjout(self):
        self.intake.set(12.5)
        self.next_state("arin")

    @state()
    def arin(self):
        self.intake.set(4.5)
        self.next_state("ardone")

    @state()
    def ardone(self):
        self.swerve.brake()
