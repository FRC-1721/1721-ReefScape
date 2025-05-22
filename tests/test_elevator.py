import pytest
from magicbot import will_reset_to
from component.elevator import Elevator
import constant.ElevatorConstants as ElevatorConstants


@pytest.fixture
def mock_motor():
    """
    Creates a mock motor that simulates a TalonFX with a built-in encoder.
    """

    class MockMotor:
        def __init__(self):
            self.output = 0  # Simulated motor output

        def set(self, value):
            self.output = value  # Store the motor output for verification

        def get_position(self):
            # Simulating a StatusSignal object that has a .value property
            return type("MockStatusSignal", (), {"value": 2.0})()

        def set_control(self, mode):
            pass

    return MockMotor()


@pytest.fixture
def elevator(mock_motor):
    """
    Creates an Elevator instance and injects a mock motor.
    """
    elevator = Elevator()
    elevator.elevatorMotor = mock_motor  # Inject the shared mock motor
    return elevator


def test_set_position(elevator):
    """
    Test that setting a goal updates the internal state.
    """
    elevator.set(5.0)
    assert elevator.x == 5.0


def test_pid_control(elevator):
    """
    Test that the PID controller attempts to correct position error.
    """
    elevator.set(5.0)  # Target position is 5.0
    elevator.execute()  # Run one control loop cycle

    # Ensure some correction is applied
    assert elevator.elevatorMotor.output != 0


def test_position_feedback(elevator):
    """
    Test the position feedback function.
    """
    assert elevator.get_position() == 2.0
