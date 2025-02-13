import wpimath
import logging
import phoenix6

from wpimath.controller import PIDController
from wpimath.controller import SimpleMotorFeedforwardMeters
from magicbot import feedback, will_reset_to
from constant.ElevatorConstants import ElevatorConstants
from utils import value_changed


class Elevator:
    """
    Robot Elevator Component
    """

    # Hardware
    elevatorMotor1: phoenix6.hardware.talon_fx.TalonFX
    elevatorMotor2: phoenix6.hardware.talon_fx.TalonFX

    x = will_reset_to(0)

    def __init__(self):
        # Initialize PID controller
        self.controller = PIDController(
            ElevatorConstants.LiftPID.P,
            ElevatorConstants.LiftPID.I,
            ElevatorConstants.LiftPID.D,
        )

        # Feedforward (optional but useful for motion control)
        self.feedforward = SimpleMotorFeedforwardMeters(
            ElevatorConstants.LiftFF.kS,
            ElevatorConstants.LiftFF.kV,
            ElevatorConstants.LiftFF.kA,
        )

        # Flags
        self._manual_mode = False  # Internal flag (default: False)

    def setup(self):
        """
        This function is automatically called by MagicBot after injection.
        """

        # Set motor2 to follow motor1
        self.elevatorMotor2.set_control(
            phoenix6.controls.follower.Follower(ElevatorConstants.Motor1ID, True)
        )

        # Reset encoders
        self.elevatorMotor1.set_position(0)  # Reset Falcon's built-in encoder

    def set(self, goal: float):
        """Set the target position for the elevator."""
        self.x = goal

    def set_manual_mode(self, enabled: bool):
        """
        Enables or disables manual mode.
        :param enabled: True to enable manual mode, False to disable.
        """
        if value_changed("elevator_manual_mode", enabled):
            logging.info(f"Elevator manual mode {'ENABLED' if enabled else 'DISABLED'}")
        self._manual_mode = enabled

    def execute(self):
        """
        Run control loop for the elevator.
        """

        # TODO Use something other than the motor itself as the encoder
        current_position = self.elevatorMotor1.get_position().value

        pid_output = self.controller.calculate(current_position, self.x)
        ff_output = self.feedforward.calculate(self.x)  # Feedforward for motion control

        output = pid_output + ff_output

        if not self._manual_mode:
            # Apply PID + FF control
            self.elevatorMotor1.set(output)
        else:
            # Manually override to direct control
            self.elevatorMotor1.set(self.x)

    def is_manual_mode(self) -> bool:
        """Returns whether manual mode is currently enabled."""
        return self._manual_mode

    @feedback
    def get_position(self) -> float:
        """Return current elevator position (for telemetry/debugging)."""
        return self.elevatorMotor1.get_position().value
