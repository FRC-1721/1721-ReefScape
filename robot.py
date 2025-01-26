#!/usr/bin/env python3

import logging
from magicbot import MagicRobot

class Robot(MagicRobot):
    """ The main class used by robotpy. This class is mandatory.
    
    The robot will run periodic tasks based on what state the robot is currently in.
    
    Robot States:
        Disabled:     The robot is currently disabled.
            - See disabledInit() and disabledPeriodic()
        Autonomous:   The robot is coded to act on its own
            - See disabledInit() and disabledPeriodic()
        Teleop:       Remote controlled, usually by a human with a joystick.
            - See teleopInit() and teleopPeriodic()
        Test:         Testing mode
            - See teleopInit() and teleopPeriodic()

    Args:
        MagicRobot (Class): The base class, which itself inherits from wpilib.RobotBase.
    """

    # This is just a general purpose counter. I am using it in this example code to allow me
    # to slowly print periodic status updates
    indexCount = 0
        
    def robotInit(self):
        """
        This method is called as soon as the robot is turned on.
        """
        super().robotInit()
    
        self.logger = logging.getLogger("Brian")
        self.logger.info("Brian's robot is initializing")

    def createObjects(self):
        """
        TBD: This method will be utilized in future commits
        """
        ...

    def disabledInit(self):
        """
        Called when disabled state starts
        """
        print("\ndisabledInit")
        self.indexCount = 0

    def disabledPeriodic(self):
        """
        The periodic code that is run in the disable state.
        
        The Amount of time each loop takes is set in the MagicRobot base class.
        It defaults to 20ms and is set with 'control_loop_wait_time = 0.020'
        """
        if self.indexCount % 250 == 0:
            print(".", end = " ")
        self.indexCount += 1
        
    def autonomousInit(self):
        """
        Called when autonomous state starts for any of the autonomous modes.
        
        The autonomous state does not use an autonomousPeriodic. Instead, it uses
        the AutonomousModeSelector (which will be utilized in a future commit)
        """
        print("\nautonomousInit")
        self.indexCount = 0
        
    def teleopInit(self):
        """
        Called when teleop state starts
        """
        print("\nteleopInit")
        self.indexCount = 0
        
    def teleopPeriodic(self):
        """
        The periodic code that is run in the teleop state.
        
        The Amount of time each loop takes is set in the MagicRobot base class.
        It defaults to 20ms and is set with 'control_loop_wait_time = 0.020'
        """
        if self.indexCount % 250 == 0:
            print(".", end = " ")
        self.indexCount += 1

    def testInit(self):
        """
        Called when test state starts
        """
        print("\ntestInit")
        self.indexCount = 0
        
    def testPeriodic(self):
        """
        The periodic code that is run in the test state.
        
        The Amount of time each loop takes is set in the MagicRobot base class.
        It defaults to 20ms and is set with 'control_loop_wait_time = 0.020'
        """
        if self.indexCount % 250 == 0:
            print(".", end = " ")
        self.indexCount += 1
    
    def robotPeriodic(self):
        """
        Called last after every state. Can be useful to always update things such as
        network tables.
        
        Add code here if you need something to always happen. Look at the base class to
        see what it updates.
        """
        super().robotPeriodic()