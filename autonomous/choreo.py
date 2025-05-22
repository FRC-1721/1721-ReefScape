import wpilib
from itertools import chain
from typing import Callable
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve
import choreo


class ChoreoAuto(AutonomousStateMachine):

    MODE_NAME = "Choreo"
    DEFAULT = True
    DISABLED = False

    swerve: Swerve
    trajectory: choreo.trajectory.SwerveTrajectory
    is_red: Callable[[], bool]

    @state(first=True)
    def correct(self):
        self.next_state_now("sample")
        initial = self.trajectory.get_initial_pose(False)
        self.swerve.target(initial)
        difference = self.swerve.get_state().pose.relativeTo(initial)
        print("------------------------------")
        print(initial)
        print(self.swerve.get_state().pose)
        print(difference)
        if (
            -0.01 < difference.x < 0.01
            and -0.01 < difference.y < 0.01
            and -2 < difference.rotation().degrees() < 2
        ):
            self.next_state_now("sample")

    @state()
    def sample(self, state_tm):
        if not self.trajectory:
            self.next_state_now("trajectory_missing")

        # if self.swerve.get_state().pose is not initial:
        #     self.next_state_now()

        sample = self.trajectory.sample_at(state_tm, self.is_red())
        if sample:
            self.swerve.target(sample)
        else:
            print("no sample?", sample)

    @state()
    def trajectory_missing(self):
        print("Choreo trajectory didn't load! Lmao!")
