from wpilib.interfaces import GenericHID

class DriverConstants:
    # controller setup
    controller = GenericHID(0)

    """
    movement axis

    FD = forward/backward
    LR = left/right
    TR = Turn
    """
    driveFD = 1
    driveLR = 0
    driveTR = 4

    # button bindings
    fieldCentricToggle = 5
    tare = 7
    brake = [2,3]


class OperatorConstants:
    # controller setup
    controller = GenericHID(1)

    # elevator bindings
    l2 = 3
    l1 = 4
    elevatorManualAxis = 5

    # intake bindings
    intake = 5
    eject = 6
    hold = 1

    # intake movement bindings
    PosOut = 2
    PosIn = 3
    intakeManualAxis = 1
    