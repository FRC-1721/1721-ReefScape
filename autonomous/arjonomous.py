import wpilib
import logging
import ntcore

from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve

# quick template for making autos


class ArjAuto(AutonomousStateMachine):

    MODE_NAME = "ArjAuto"
    DEFAULT = True
    DISABLED = False

    # Components
    swerve: Swerve

    @timed_state(duration=0.5, next_state="armove", first=True)
    def arwait(self, tm, initial_call):
        pass

    @state()
    def armove(self, tm, initial_call):
        if initial_call:
            # This is the first time this function runs
            self.startx = self.swerve.pose()[0] if wpilib.RobotBase.isReal() else 1.721
            logging.debug(f"ArjAuto set startx to {self.startx}")

        distance_driven = (
            self.swerve.pose()[0] - self.startx  # Real Robot
            if wpilib.RobotBase.isReal()
            else ntcore.NetworkTableInstance.getDefault()  # Robot is existential
            .getTable("SmartDashboard")
            .getEntry("Field/Robot")
            .getDoubleArray(0.0)[0]  # X pose in robotpose
        )
        logging.info(f"Distance driven {distance_driven}")

        if distance_driven < 1.0:
            self.swerve.go(0.1, 0, 0, False)
        else:
            self.next_state("ardone")

    @state()
    def ardone(self, tm, initial_call):
        self.swerve.brake()
