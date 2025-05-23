import wpilib
import logging
import ntcore

from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve
from component.intake import Intake

from constant import IntakeConstants, ElevatorConstants

# quick template for making autos


class StraightL2Auto(AutonomousStateMachine):

    MODE_NAME = "Straight - L2"
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

        if distance_driven < 1.4:
            self.swerve.go(0.5, 0, 0, False)
        else:
            self.next_state("arjown")

    @timed_state(duration=5, next_state="arject")
    def arjown(self):
        self.intake.set(IntakeConstants.PosOut)
        self.elevator.set(ElevatorConstants.Setpoint.L2)

    @timed_state(duration=1, next_state="ardone")
    def arject(self):
        self.intake.eject()

    @state()
    def ardone(self):
        self.swerve.brake()
