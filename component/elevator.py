import phoenix6
import wpimath
from wpilib import MotorControllerGroup
from magicbot import feedback, will_reset_to


class Elevator:
    elevatorMotor1: phoenix6.hardware.talon_fx.TalonFX
    elevatorEncoder: phoenix6.hardware.CANcoder

    x = will_reset_to(0)

    # TODO: Adjust PID
    controller = wpimath.controller.PIDController(1, 0, 0)

    def set(self, goal):
        self.x = goal

    def execute(self):
        elevatorMotor1.set(
            self.controller.calculate(elevatorEncoder.get_position(), self.x)
        )
