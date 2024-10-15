import re
from enum import Enum


# matchers
class Matchers(str, Enum):
    value: str

    PREV_TOKEN = '[{};]'
    FIRST_WORD_NO_LETTER = PREV_TOKEN + '\s+'
    FIRST_WORD_LOWER = FIRST_WORD_NO_LETTER + '([a-z_][A-Za-z]*)'
    FIRST_WORD_UPPER = FIRST_WORD_NO_LETTER + '([A-Z_][A-Za-z]*)'
    VARIABLE_NAME = FIRST_WORD_UPPER + '\s+'
    PUBLIC_FIELDS_AND_METHODS = FIRST_WORD_LOWER + '\.'
    PUBLIC_FIELDS_AND_METHODS_INCOMPLETE = PUBLIC_FIELDS_AND_METHODS + '([A-Za-z]+)'
    NEW_OR_BUILDER = FIRST_WORD_UPPER + '\s+\S+=\s+'
    NEW = NEW_OR_BUILDER + 'n'

class CompletionContext:
    def __init__(self, lines, line, col):
        contextLine = self.get_context_string(lines, line, col)
        varNameMatch = re.compile(Matchers.VARIABLE_NAME).fullmatch(contextLine)
        firstWordUpper = re.compile(Matchers.FIRST_WORD_UPPER).fullmatch(contextLine)
        pubFldsAndMthds = re.compile(Matchers.PUBLIC_FIELDS_AND_METHODS).fullmatch(contextLine)
        pubFldsAndMthdsIncomplt = re.compile(Matchers.PUBLIC_FIELDS_AND_METHODS_INCOMPLETE).fullmatch(contextLine)
        newOrBuilder = re.compile(Matchers.NEW_OR_BUILDER).fullmatch(contextLine)
        newMatch = re.compile(Matchers.NEW).fullmatch(contextLine)
        if re.compile(Matchers.FIRST_WORD_NO_LETTER).fullmatch(contextLine):
            self.context_string = Matchers.FIRST_WORD_NO_LETTER
        elif re.compile(Matchers.FIRST_WORD_LOWER).fullmatch(contextLine):
            self.context_string = Matchers.FIRST_WORD_LOWER
        elif firstWordUpper is not None:
            self.word_before_cursor = firstWordUpper.groups()[0]
            self.context_string = Matchers.FIRST_WORD_UPPER
        elif varNameMatch is not None:
            self.declaredType = varNameMatch.groups()[0]
            self.context_string = Matchers.VARIABLE_NAME
        elif pubFldsAndMthds is not None:
            self.word_before_period = pubFldsAndMthds.groups()[0]
            self.context_string = Matchers.PUBLIC_FIELDS_AND_METHODS
        elif pubFldsAndMthdsIncomplt is not None:
            self.word_before_period = pubFldsAndMthdsIncomplt.groups()[0]
            self.word_before_cursor = pubFldsAndMthdsIncomplt.groups()[1]
            self.context_string = Matchers.PUBLIC_FIELDS_AND_METHODS_INCOMPLETE
        elif newOrBuilder is not None:
            self.declaredType = newOrBuilder.groups()[0]
            self.context_string = Matchers.NEW_OR_BUILDER
        elif newMatch is not None:
            self.declaredType = newMatch.groups()[0]
            self.context_string = Matchers.NEW


    def get_context_string(self, lines, line, col):
        left_text = lines[line][:col]
        upper_lines = lines[:line]
        beforeText = ''.join(upper_lines) + left_text
        tokens = list(re.finditer('\{|\}|;', beforeText))
        if len(tokens) > 0:
            lastToken = tokens[-1]
            return beforeText[lastToken.start():]
        else:
            return beforeText


