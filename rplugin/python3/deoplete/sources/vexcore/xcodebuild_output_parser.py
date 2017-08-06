class XcodebuildOutputParser():
    def __init__(self, input, toolchain):
        self.input = input
        self.toolchain = toolchain

    def parse_input(self):
        self.flags = self.find_compile_flags()
        print(self.flags)

    def find_compile_flags(self):
        compile_cmd = f"    {self.toolchain}/usr/bin/swiftc"
        return [x.strip().split(" ") for x in self.input.splitlines() if x.startswith(compile_cmd)]

