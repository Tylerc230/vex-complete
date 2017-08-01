import os
import re
import sys
import json
import vexcore

from .base import Base

from deoplete.util import charpos2bytepos
from deoplete.util import error

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'Swift'
        self.mark = '[Swift]'
        self.filetypes = ['swift']
        self.input_pattern = r'(?:\b[^\W\d]\w*|[\]\)])(?:\.(?:[^\W\d]\w*)?)*\(?'
        self.rank = 500
        
        self.temp_file_directory = "/tmp/vexcomplete/"

        if not os.path.exists(self.temp_file_directory):
            os.makedirs(self.temp_file_directory)

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1

    def gather_candidates(self, context):
        line = self.vim.current.window.cursor[0]
        column = self.vim.current.window.cursor[1]

        filename = self.vim.call('expand', '%:p').split('/')[-1]
        buf = self.vim.current.buffer
        offset = self.vim.call('line2byte', line) + \
            charpos2bytepos('utf-8', context['input'], column) - 1

        completion = Completion(source_file=filename)
        result = completion.completion_at_offset(offse)
        return result

        # source = '\n'.join(buf)
        # tmp_path = self.temp_file_directory + filename
        # tmp_file = open(tmp_path, 'w+')
        # tmp_file.write(source)
        # tmp_file.close()

        # request = urllib2.Request("http://localhost:8081/complete")
        # request.add_header("X-Path", tmp_path)
        # request.add_header("X-Offset", offset - 1)
        # request.add_header("X-File", filename)
        # try:
            # response = urllib2.urlopen(request).read().decode('utf-8')
            # return self.identifiers_from_result(json.loads(response))
        # except:
            # return []


    def identifiers_from_result(self, result):
        out = []

        candidates = []
        longest_desc_length = 0
        longest_desc = ''
        for complete in result:
            candidates.append(complete)

            desc_len = len(complete['descriptionKey'])

            if desc_len > longest_desc_length:
                longest_desc = complete['descriptionKey']
                longest_desc_length = desc_len

        for completion in candidates:
            description = completion['descriptionKey']
            _type = completion['typeName']
            abbr = description + ' : ' + _type.rjust((len(description) - longest_desc_length) + 3)
            info = _type

            candidate = dict(word=description,
                              abbr=abbr,
                              dup=1
                              )

            out.append(candidate)

        return out

