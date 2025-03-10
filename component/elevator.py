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

    controller = Const.Controller
    feedforward = Const.FFController

    def __init__(self):
        # Flags
        self.x = Const.Setpoint.HOME
        self._manual_mode = False  # Internal flag (default: False)

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
        # if self.elevatorLimit.get(): self.elevatorMotor.set_position(0)
        # if self.get_position() <= 0 and not self.elevatorLimit.get():
        #    self.elevatorMotor.set_position(5)

        current_position = self.elevatorMotor.get_position().value

        pid_output = self.controller.calculate(current_position, self.x)
        ff_output = self.feedforward.calculate(self.x)  # Feedforward for motion control
        # ff_output = 0

        output = pid_output + ff_output

        # Apply PID + FF control
        # print(f"{output} --> {Const.clamp(output)}")
        if not (self.get_position() <= 0 and output <= 0):
            self.elevatorMotor.set(Const.clamp(output))

    def threshhold(self, value, threshhold=5, dampen=0.3):
        return value * (1 if value <= threshhold else dampen)

    @feedback()
    def limit(self) -> bool:
        return self.elevatorLimit.get()

    @feedback
    def goal(self) -> float:
        return self.x

    @feedback
    def is_manual_mode(self) -> bool:
        """Returns whether manual mode is currently enabled."""
        return self._manual_mode

    @feedback
    def get_position(self) -> float:
        """Return current elevator position (for telemetry/debugging)."""
        return self.elevatorMotor.get_position().value
