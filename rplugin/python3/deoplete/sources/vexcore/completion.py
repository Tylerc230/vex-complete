from .sourcekitd.capi import Config, UIdent
from .sourcekitd.request import request_sync
from .xcodebuild_output_parser import CompilerFlags
from .non_frontend_flags import non_frontend_flags

class Completion():
    request_key = "source.request.codecomplete"

    def __init__(self, logger):
        self.logger = logger
        self.xcodebuild_output = CompilerFlags(self.logger, excluded_flags = non_frontend_flags)
        self.xcodebuild_output.parse_input()

    def completion_at_offset(self, byte_offset, source_file, text):
        req = { 
                'key.request': UIdent(self.request_key),
                'key.offset': byte_offset
                }
        if not text == None:
            self.logger.info("vex text based completion")
            self.logger.debug(f"vex text: {text}")
            req['key.sourcetext'] = text

        req['key.sourcefile'] = source_file
        req['key.compilerargs'] = self.xcodebuild_output.flags
        self.logger.debug(f"vex request {req}")
        resp = request_sync(req)
        py_obj =  resp.get_payload().to_python_object()
        results = py_obj['key.results']
        candidates = map(lambda d: d['key.sourcetext'], results)
        return list(candidates)


