import wpimath
import logging
import phoenix6

from wpimath.controller import PIDController
from wpimath.controller import ElevatorFeedforward
from magicbot import feedback, will_reset_to
import constant.ElevatorConstants as Const
import util


class Elevator:
    """
    Robot Elevator Component
    """

    # Hardware
    elevatorMotor: Const.MotorClass
    elevatorMotor2: Const.MotorClass
    elevatorLimit: Const.LimitClass

    def __init__(self):
        # Flags
        self.x = Const.Setpoint.HOME

    def setup(self):
        """
        This function is automatically called by MagicBot after injection.
        """

        ...

    def set(self, goal: float):
        """Set the target position for the elevator."""
        self.x = goal

    def execute(self):
        """
        Run control loop for the elevator.
        """

        self.elevatorMotor.set_control(Const.PIDControl(self.x))

        # # TODO fix this
        # # keep going down if you think you're at zero and the limit is not pressed
        # if not self.limit() and self.get_position() == 0:
        #     self.elevatorMotor.set_position(5)

    def threshhold(self, value, threshhold=5, dampen=0.3):
        return value * (1 if value <= threshhold else dampen)

    @feedback()
    def limit(self) -> bool:
        return self.elevatorLimit.get()

    def isReady(self, offset=0.1):
        return abs(self.get_position() - self.x) < offset

    @feedback
    def goal(self) -> float:
        return self.x

    @feedback
    def get_position(self) -> float:
        """Return current elevator position (for telemetry/debugging)."""
        return self.elevatorMotor.get_position().value
