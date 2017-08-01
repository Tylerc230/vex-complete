from .sourcekitd.capi import Config, UIdent
from .sourcekitd.request import request_sync

class Completion():
    request_key = "source.request.codecomplete"

    def __init__(self, text=None, source_file=None):
        self.source_file = source_file
        self.text = text

    def completion_at_offset(self, byte_offset):
        req = { 
                'key.request': UIdent(self.request_key),
                'key.offset': byte_offset
                }
        if not self.text == None:
            req['key.sourcetext'] = self.text
            sourcefile = "46F57330-59A6-490C-A782-2E3C3C0DC5E0.swift"
        elif not self.source_file == None:
            sourcefile = self.source_file
        else:
            raise RuntimeError("Must do completion on file or text")
        req['key.sourcefile'] = sourcefile
        req['key.compilerargs'] = ["-c", sourcefile]
        resp = request_sync(req)
        py_obj =  resp.get_payload().to_python_object()
        results = py_obj['key.results']
        candidates = map(lambda d: d['key.sourcetext'], results)
        return list(candidates)


