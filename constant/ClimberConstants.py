import phoenix6
import wpilib


MotorClass = phoenix6.hardware.talon_fx.TalonFX
Motor = [MotorID := 32]

SolenoidClass = wpilib.Solenoid
Solenoid = [PCMID := 59, PCMType := wpilib.PneumaticsModuleType.CTREPCM, Channel := 4]

ClimbSpeed = 0.5
UnclimbSpeed = -0.5

FreeSpeed = 1
