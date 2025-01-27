import phoenix6
import wpimath
from rev import SparkAbsoluteEncoder
from wpilib import MotorControllerGroup
from magicbot import feedback, will_reset_to


class Elevator:
    elevatorMotor1: phoenix6.hardware.talon_fx.TalonFX
    elevatorEncoder: SparkAbsoluteEncoder

    x = will_reset_to(0)

    # TODO: Adjust PID
    controller = wpimath.controller.PIDController(1, 0, 0)

    def set(self, goal):
        self.x = goal

    def execute(self):
        self.elevatorMotor1.set(
            self.controller.calculate(self.elevatorEncoder.getPosition(), self.x)
        )
