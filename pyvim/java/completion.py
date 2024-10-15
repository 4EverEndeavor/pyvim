import weakref
import os
import re

from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.document import Document
from . import java_bones
from .context import CompletionContext, Matchers

class JavaCompleter(Completer):
    '''
    Completion for java files
    '''
    def __init__(self, location):
        self.location = location


    def get_completions(self, document: Document, complete_event):
        breakpoint()
        self.word_before_cursor = document.get_word_before_cursor()
        self.col = document.cursor_position_col
        self.line = document.cursor_position_row
        self.lines = document.lines
        self.context = CompletionContext(self.lines, self.line, self.col)

        if self.line == 0:
            word = self.get_package_line()
            yield Completion(word, start_position=-len(self.word_before_cursor))

        if self.context.context_string == Matchers.FIRST_WORD_NO_LETTER:
            words = self.get_first_words()
            for w in words:
                yield Completion(w, start_position=-len(self.word_before_cursor))

        if self.context.context_string == Matchers.FIRST_WORD_LOWER:
            words = self.get_first_words_lower()
            for w in words:
                if w.startswith(self.word_before_cursor) and w != self.word_before_cursor:
                    yield Completion(w, start_position=-len(self.word_before_cursor))

        if self.context.context_string == Matchers.FIRST_WORD_UPPER:
            words = self.get_first_words_upper()
            for w in words:
                yield Completion(w, start_position=-len(self.word_before_cursor))

        if self.context.context_string == Matchers.PUBLIC_FIELDS_AND_METHODS:
            fieldsMethodCompletion = self.get_words_after_period()
            for method in fieldsMethodCompletion['methods']:
                yield Completion(method['name'], start_position=0,
                    display=method['display'], display_meta=method['displayMeta'])
            for field in fieldsMethodCompletion['fields']:
                displayStr = field['name'] + '  ' + field['type']
                displayMeta = field['name'] + '  meta'
                yield Completion(field['name'], start_position=0, display=displayStr, display_meta=displayMeta)

        if self.context.context_string == Matchers.PUBLIC_FIELDS_AND_METHODS_INCOMPLETE:
            fieldsMethodCompletion = self.get_words_after_period()
            for method in fieldsMethodCompletion['methods']:
                if method['name'].startswith(self.context.word_before_cursor):
                    yield Completion(method['name'], start_position=-len(self.context.word_before_cursor),
                        display=method['display'], display_meta=method['displayMeta'])
            for field in fieldsMethodCompletion['fields']:
                displayStr = field['name'] + '  ' + field['type']
                displayMeta = field['name'] + '  meta'
                if field['name'].startswith(self.context.word_before_cursor):
                    yield Completion(field['name'], start_position=-len(self.context.word_before_cursor),
                        display=displayStr, display_meta=displayMeta)



    def get_package_line(self):
        package_line = 'package ' + self.get_package_name() + ';'
        return package_line


    def get_package_name(self):
        package_name = os.getcwd().split('java')[1][1:].replace('/','.')
        return package_name


    def get_file_name(self):
        file_name = self.location.split('.')[0]
        return file_name


    def get_first_words(self):
        return java_bones.keywords + java_bones.primitiveTypes


    def get_first_words_lower(self):
        textBefore = self.get_text_before()
        words = re.findall('[a-z_][A-Za-z]+', textBefore)
        return set(words + self.get_first_words())


    def get_first_words_upper(self):
        return java_bones.get_all_class_names(self.word_before_cursor)

    def get_words_after_period(self):
        return java_bones.get_fields_and_methods(self.get_java_type())


    def get_text_before(self):
        lines_above = self.lines[:self.line]
        current_line = self.lines[self.line]
        left_line = current_line[:self.col]
        text_above = ''.join(lines_above) + left_line
        return text_above


    def get_java_type(self):
        firstChar = self.context.word_before_period[0]
        # If it's upper case, treating as type
        if re.compile('[A-Z]').fullmatch(firstChar):
            return self.context.word_before_period
        # otherwise, we need to find the declaration
        text_above = self.get_text_before()
        p = '([A-Z][A-Za-z]+) ' + self.context.word_before_period
        declarations = list(re.finditer(p, text_above))
        declaration = declarations[-1]
        return declaration.groups()[0]


