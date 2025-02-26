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

    def set_manual_mode(self, enabled: bool):
        """
        Enables or disables manual mode.
        :param enabled: True to enable manual mode, False to disable.
        """
        if util.value_changed("elevator_manual_mode", enabled):
            logging.info(f"Elevator manual mode {'ENABLED' if enabled else 'DISABLED'}")
            print(f"Elevator manual mode {'ENABLED' if enabled else 'DISABLED'}")
            if not enabled:
                self.x = self.get_position()
        self._manual_mode = enabled

    def execute(self):
        """
        Run control loop for the elevator.
        """

        # TODO Use something other than the motor itself as the encoder
        current_position = self.elevatorMotor.get_position().value

        pid_output = self.controller.calculate(current_position, self.x)
        ff_output = self.feedforward.calculate(self.x)  # Feedforward for motion control
        # ff_output = 0

        output = pid_output + ff_output

        if not self._manual_mode:
            # Apply PID + FF control
            # print(f"{output} --> {Const.clamp(output)}")
            self.elevatorMotor.set(Const.clamp(output))
        else:
            # Manually override to direct control
            self.elevatorMotor.set(self.x)

    def isReady(self, offset=0.1):
        return abs(self.get_position() - self.x) < offset

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
