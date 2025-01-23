import phoenix6
from magicbot import feedback, will_reset_to


class Elevator:
    elevatorMotor1: phoenix6.hardware.TalonFX
    elevatorMotor2: phoenix6.hardware.TalonFX
    elevatorEncoder: phoenix6.hardware.CANcoder

    x = will_reset_to(0)

    # motor group
    self.motorGroup = wpilib.MotorControllerGroup(elevatorMotor1, elevatorMotor2)

    # TODO: Adjust PID
    controller = wpimath.controller.PIDController(1, 0, 0)

    def set(self, goal):
        self.x = goal

    def execute(self):
        motorGroup.set(
            self.controller.calculate(elevatorEncoder.get_position(), self.x)
        )
