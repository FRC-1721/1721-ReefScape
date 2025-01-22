import phoenix6
from magicbot import feedback, will_reset_to


class Elevator:
    elevatorMotor1: phoenix6.hardware.TalonFX
    elevatorMotor2: phoenix6.hardware.TalonFX

    x = will_reset_to(0)

    def move(self, amount):
        self.x = amount

    def execute(self):
        motor.set(self.x)
