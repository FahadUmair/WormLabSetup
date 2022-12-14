from seedemu.core.Emulator import Emulator
from seedemu.core import Registry
from os import mkdir, chdir, getcwd, path
from shutil import rmtree
from sys import stderr, exit

class Compiler:
    """!
    @brief The Compiler base class.

    Compiler takes the rendered result and compiles them to working emulators.
    """

    def _doCompile(self, emulator: Emulator):
        """!
        @brief Compiler driver implementation.

        This method should be implemented by the compiler driver. The driver
        class can assume that the current working directory is the output
        folder.

        @param emulator emulator object.
        """
        raise NotImplementedError('_doCompile not implemented.')

    def getName(self) -> str:
        """!
        @brief Get the name of compiler driver.

        @returns name of the driver.
        """
        raise NotImplementedError('getName not implemented.')

    def compile(self, emulator: Emulator, output: str, override: bool = False):
        """!
        @brief Compile the simulation.

        @param emulator emulator object.
        @param output output directory path.
        @param override (optional) override the output folder if it already
        exist. False by default.
        """
        assert emulator.rendered(), 'Simulation needs to be rendered before compile.'

        cur = getcwd()
        if path.exists(output):
            if override:
                self._log('output folder "{}" already exist, overriding.'.format(output))
                rmtree(output)
            else:
                self._log('output folder "{}" already exist. Set "override = True" when calling compile() to override.'.format(output))
                exit(1)
        mkdir(output)
        chdir(output)
        self._doCompile(emulator)
        chdir(cur)

    def _log(self, message: str) -> None:
        """!
        @brief Log to stderr.

        @param message message.
        """
        print("== {}Compiler: {}".format(self.getName(), message), file=stderr)
