import subprocess
import logging
logger = logging.getLogger(__name__)
class CompilerFlags():
    def __init__(self, toolchain="/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain", input=None, excluded_flags=None):
        self.excluded_flags = excluded_flags
        if input == None:
            self.input = self._xcodebuild()
        else:
            self.input = input
        self.toolchain = toolchain

    def parse_input(self):
        self.flags = self._find_compile_flags()

    def _find_compile_flags(self):
        compile_cmd = f"    {self.toolchain}/usr/bin/swiftc"
        lines = [x.strip() for x in self.input.splitlines() if x.startswith(compile_cmd)][0]
        return [arg for arg in lines.split(" ") if arg not in self.excluded_flags]

    def _xcodebuild(self):
        try:
            output = subprocess.check_output(["xcodebuild", "clean", "build", "-dry-run", "-destination", "platform=iOS Simulator,name=iPhone 5s", "-scheme", "VimTesting"])
            return output.decode("utf-8")
        except subprocess.CalledProcessError as output:
            logger.error(f"Failed to get xcodebuild output: {output}")
            return ""



