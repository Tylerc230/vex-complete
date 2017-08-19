import subprocess
from deoplete.logger import LoggingMixin

class CompilerFlags():
    def __init__(self, logger, toolchain=None, input=None, excluded_flags=None):
        self.logger = logger
        self.excluded_flags = excluded_flags
        if input == None:
            self.input = self._xcodebuild()
        else:
            self.input = input

        if toolchain == None:
            self.toolchain = self._xcode_select()
        else:
            self.toolchain = toolchain
        self.logger.info(f"vex toolchain {self.toolchain}")

    def parse_input(self):
        self.flags = self._find_compile_flags()
        self.logger.debug(f"vex xcodebuild flags {self.flags}")

    def _find_compile_flags(self):
        compile_cmd = f"    {self.toolchain}/usr/bin/swiftc"
        lines = [x.strip() for x in self.input.splitlines() if x.startswith(compile_cmd)][0]
        return [arg for arg in lines.split(" ") if arg not in self.excluded_flags]

    def _xcode_select(self):
        xcode_base = self._get_output(['xcode-select', '-p' ]).strip()
        return  xcode_base + "/Toolchains/XcodeDefault.xctoolchain"


    def _xcodebuild(self):
        return self._get_output(["xcodebuild", "clean", "build", "-dry-run", "-destination", "platform=iOS Simulator,name=iPhone 5s", "-scheme", "VimTesting"])

    def _get_output(self, cmd):
        try:
            output = subprocess.check_output(cmd)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as output:
            self.logger.error(f"Failed to get {cmd} output: {output}")
            return ""




