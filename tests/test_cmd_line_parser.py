from vexcore.xcodebuild_output_parser import XcodebuildOutputParser
class TestCommandLineParser():
    toolchain = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain"

    def test_parse_project(self):
        output = self.read_xcodebuild_output() 
        parser = XcodebuildOutputParser(output, self.toolchain)
        parser.parse_input()


    def read_xcodebuild_output(self):
        with open("./dry-run.txt") as output_file:
            output_txt = output_file.read()
        return output_txt

