from .sourcekitd.capi import Config, UIdent
from .sourcekitd.request import request_sync
from .xcodebuild_output_parser import CompilerFlags
from .non_frontend_flags import non_frontend_flags

class Completion():
    request_key = "source.request.codecomplete"

    def __init__(self, logger, text=None, source_file=None):
        self.logger = logger
        self.source_file = source_file
        self.text = text
        self.xcodebuild_output = CompilerFlags(self.logger, excluded_flags = non_frontend_flags)
        self.xcodebuild_output.parse_input()

    def completion_at_offset(self, byte_offset):
        req = { 
                'key.request': UIdent(self.request_key),
                'key.offset': byte_offset
                }
        if not self.text == None:
            self.logger.info("vex text based completion")
            self.logger.debug(f"vex text: {self.text}")
            req['key.sourcetext'] = self.text

        if self.source_file == None:
            sourcefile = "46F57330-59A6-490C-A782-2E3C3C0DC5E0.swift"
        else:
            sourcefile = self.source_file

        req['key.sourcefile'] = sourcefile
        req['key.compilerargs'] = self.xcodebuild_output.flags
        self.logger.debug(f"vex request {req}")
        resp = request_sync(req)
        py_obj =  resp.get_payload().to_python_object()
        results = py_obj['key.results']
        candidates = map(lambda d: d['key.sourcetext'], results)
        return list(candidates)


