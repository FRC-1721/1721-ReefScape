import wpilib
from itertools import chain
from magicbot import AutonomousStateMachine, state, timed_state
from component.swerve import Swerve

# quick template for making autos


class EmacsAuto(AutonomousStateMachine):

    MODE_NAME = "Emacs"
    DEFAULT = True
    DISABLED = False

    swerve: Swerve

    @timed_state(duration=0.5, next_state="emacs", first=True)
    def doom(self, tm, initial_call):
        self.swerve.brake()
        if initial_call:
            print("")
            print("Warning: due to a long standing Gtk+ bug")
            print("https://gitlab.gnome.org/GNOME/gtk/issues/221")
            print(
                "Emacs might crash when run in daemon mode and the X11 connection is unexpectedly lost."
            )
            print(
                "Using an Emacs configured with --with-x-toolkit=lucid does not have this problem."
            )
            print("Starting Doom Emacs in daemon mode...")

    @timed_state(duration=1.721, next_state="packages")
    def emacs(self, tm, initial_call):
        if initial_call:
            print("Starting Emacs daemon.")

    @state()
    def packages(self, tm, initial_call):
        if initial_call:
            print("Doom loaded 200 packages across 45 modules in 0.721s")
