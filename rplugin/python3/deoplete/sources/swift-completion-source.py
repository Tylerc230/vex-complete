import os
import re
import sys
import json
from .base import Base

from deoplete.util import charpos2bytepos
from deoplete.util import error


path = os.path.dirname(__file__)
sys.path.append(path)
from  vexcore.completion import Completion

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

        filepath = self.vim.call('expand', '%:p')
        buf = self.vim.current.buffer
        offset = self.vim.call('line2byte', line) + \
            charpos2bytepos('utf-8', context['input'], column) - 1

        completion = Completion(source_file=filepath)
        result = completion.completion_at_offset(offset)
        self.debug(f"vex {result}")
        return result


