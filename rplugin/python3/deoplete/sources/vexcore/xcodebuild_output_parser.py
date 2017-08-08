import subprocess
import logging
logger = logging.getLogger(__name__)
class CompilerFlags():
    def __init__(self, toolchain="/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain", input=None):
        if input == None:
            self.input = self._xcodebuild()
        else:
            self.input = input
        self.toolchain = toolchain

    def parse_input(self):
        self.flags = self._find_compile_flags()

    def _find_compile_flags(self):
        compile_cmd = f"    {self.toolchain}/usr/bin/swiftc".encode()
        return [x.strip().split(b" ") for x in self.input.splitlines() if x.startswith(compile_cmd)]

    def _xcodebuild(self):
        try:
            return subprocess.check_output(["xcodebuild", "clean", "build", "-dry-run", "-destination", "platform=iOS Simulator,name=iPhone 5s", "-scheme", "VimTesting"])
        except subprocess.CalledProcessError as output:
            logger.error(f"Failed to get xcodebuild output: {output}")
            return ""



