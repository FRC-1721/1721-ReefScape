import phoenix6
import wpimath
from rev import SparkAbsoluteEncoder
from wpilib import MotorControllerGroup
from magicbot import feedback, will_reset_to
from constant.ElevatorConstants import P, I, D, F


class Elevator:
    elevatorMotor1: phoenix6.hardware.talon_fx.TalonFX
    elevatorEncoder: SparkAbsoluteEncoder

    x = will_reset_to(0)

    # TODO: Adjust PID
    controller = wpimath.controller.PIDController(P, I, D, F)

    def set(self, goal):
        self.x = goal

    def execute(self):
        self.elevatorMotor1.set(
            self.controller.calculate(self.elevatorEncoder.getPosition(), self.x)
        )
