import pytest
from wpimath.geometry import Pose2d, Rotation2d
from phoenix6.swerve.requests import FieldCentric

from component.swerve import Swerve

import constant.DriveConstants as DriveConstants


@pytest.fixture
def swerve():
    return Swerve()


def test_go(swerve):
    """
    Test that the swerve component generates the correct request when go is called.
    """

    swerve.go(1.0, 0.0, 0.5, field_centric=True)
    request = swerve.request

    assert request.velocity_x == pytest.approx(1.0 * DriveConstants.max_vel)
    assert request.velocity_y == pytest.approx(0.0 * DriveConstants.max_vel)
    assert request.rotational_rate == pytest.approx(0.5 * DriveConstants.max_rot)
    assert isinstance(request, FieldCentric)


def test_real_pose_feedback(swerve):
    """
    Test the pose feedback function.

    Test written by Joe
    """

    pose = Pose2d(2.0, 3.0, Rotation2d.fromDegrees(45))
    swerve.get_state = lambda: type("State", (), {"pose": pose})()  # Mock get_state
    assert swerve.pose() == [pose.X(), pose.Y(), pose.rotation().degrees()]


def test_sim_pose_feedback(swerve):
    """
    Test the simulated pose feedback function.

    Test written by Joe
    """

    pose = Pose2d(2.0, 3.0, Rotation2d.fromDegrees(45))
    swerve.sim_pose = pose
    assert swerve.pose() == [pose.X(), pose.Y(), pose.rotation().degrees()]
