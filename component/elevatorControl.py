# import magic
from magicbot import StateMachine, state, timed_state

# import constants
from constant import IntakeConstants as intconst
from constant import ElevatorConstants as eliConst

# import components
from component.elevator import Elevator
from component.intake import Intake


class ElevatorControl(StateMachine):
    elevator: Elevator
    intake: Intake

    def start(self, level):
        self.level = level
        self.engage()

    @state(first=True)
    def lift(self):
        self.elevator.set(self.level)

        if self.elevator.isReady():
            self.next_state_now("out")

    @state(must_finish=True)
    def out(self):
        self.intake.set(intconst.PosOut)

        if self.intake.isReady(intconst.PosOut):
            self.next_state_now("blow")

    @timed_state(duration=1, must_finish=True)
    def blow(self):
        self.intake.eject()

        self.next_state("inwards")

    @state(must_finish=True)
    def inwards(self):
        self.intake.set(intconst.PosIn)

        if self.intake.isReady(intconst.PosIn):
            self.next_state_now("down")

    @timed_state(duration=1)
    def down(self):
        self.elevator.set(eliConst.HOME)
