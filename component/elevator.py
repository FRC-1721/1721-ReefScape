import wpimath
import logging
import phoenix6

from wpimath.controller import PIDController
from wpimath.controller import ElevatorFeedforward
from magicbot import feedback, will_reset_to
from constant.ElevatorConstants import Constants, Setpoints
import util


class Elevator:
    """
    Robot Elevator Component
    """

    # Hardware
    elevatorMotor: phoenix6.hardware.talon_fx.TalonFX
    elevatorMotor2: phoenix6.hardware.talon_fx.TalonFX

    x = will_reset_to(Setpoints.HOME)

    def __init__(self):
        # Initialize PID controller
        self.controller = PIDController(
            Constants.LiftPID.P,
            Constants.LiftPID.I,
            Constants.LiftPID.D,
        )

        # self.feedforward = SimpleMotorFeedforwardMeters(
        #     Constants.LiftFF.kS,
        #     Constants.LiftFF.kV,
        #     Constants.LiftFF.kA,
        # )

        # Feedforward (optional but useful for motion control)
        self.feedforward = ElevatorFeedforward(
            Constants.LiftFF.kS,
            Constants.LiftFF.kG,
            Constants.LiftFF.kV,
            Constants.LiftFF.kA,
        )

        # Flags
        self._manual_mode = False  # Internal flag (default: False)

        # Clamp
        self.clamp = util.clamp(Constants.down, Constants.up)

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
            print(f"{output} --> {self.clamp(output)}")
            self.elevatorMotor.set(self.clamp(output))
        else:
            # Manually override to direct control
            self.elevatorMotor.set(self.x)

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
