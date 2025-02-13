import phoenix6
import wpimath
from rev import SparkAbsoluteEncoder
from wpilib import MotorControllerGroup
from magicbot import feedback, will_reset_to
from wpimath.controller import PIDController, SimpleMotorFeedforward
from constant.ElevatorConstants import ElevatorConstants


class Elevator:
    elevatorMotor1: phoenix6.hardware.talon_fx.TalonFX

    x = will_reset_to(0)

    def __init__(self):
        # Using structured PID values
        self.controller = PIDController(
            ElevatorConstants.LiftPID.P,
            ElevatorConstants.LiftPID.I,
            ElevatorConstants.LiftPID.D,
        )

        # Using structured Feedforward values
        self.feedforward = SimpleMotorFeedforward(
            ElevatorConstants.LiftFF.kS,
            ElevatorConstants.LiftFF.kV,
            ElevatorConstants.LiftFF.kA,
        )

    def set(self, goal: float):
        """Set the target position for the elevator."""
        self.x = goal

    def execute(self):
        """Run control loop for the elevator."""
        # TODO: Replace with actual encoder when available
        current_position = (
            self.elevatorEncoder.getPosition()
            if hasattr(self, "elevatorEncoder")
            else 0
        )

        pid_output = self.controller.calculate(current_position, self.x)
        ff_output = self.feedforward.calculate(self.x)  # Velocity-based feedforward

        output = pid_output + ff_output

        # Ensure motor safety
        self.elevatorMotor1.set(output)

    @feedback
    def get_position(self) -> float:
        """Return current elevator position (for telemetry/debugging)."""
        return (
            self.elevatorEncoder.getPosition()
            if hasattr(self, "elevatorEncoder")
            else 0
        )
