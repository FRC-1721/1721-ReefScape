import phoenix6
import wpimath
from wpimath.controller import PIDController
from wpimath.controller import SimpleMotorFeedforwardMeters
from magicbot import feedback, will_reset_to
from constant.ElevatorConstants import ElevatorConstants


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

    def execute(self):
        """
        Run control loop for the elevator.
        """

        # Using the internal encoder TODO: change!
        current_position = self.elevatorMotor1.get_position().value

        pid_output = self.controller.calculate(current_position, self.x)
        ff_output = self.feedforward.calculate(self.x)  # Feedforward for motion control

        output = pid_output + ff_output

        # Apply output to the motor
        self.elevatorMotor1.set(output)

    @feedback
    def get_position(self) -> float:
        """Return current elevator position (for telemetry/debugging)."""
        return self.elevatorMotor1.get_position().value
