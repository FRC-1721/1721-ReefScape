import wpilib
from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve

# quick template for making autos


class ChoreoAuto(AutonomousStateMachine):

    MODE_NAME = "Choreo"
    DEFAULT = True
    DISABLED = False

    swerve: Swerve
    trajectory: ...  # TODO what is the correct type
    is_red: ...  # TODO what is the correct type

    @state(first=True)
    def packages(self, state_tm):
        if not self.trajectory:
            self.next_state_now("trajectory_missing")

        sample = self.trajectory.sample_at(state_tm, self.is_red())
        if sample:
            self.swerve.trajectory(sample)
        else:
            print("no sample?")

    @state()
    def trajectory_missing(self):
        print("Choreo trajectory didn't load! Lmao!")
