import json
import subprocess
import re
from subprocess import CompletedProcess
from difflib import SequenceMatcher as SM


class JavapMatchers:
    def __init__(self):
        self.keywords = ['public', 'private', 'protected', 'final', 'import']
        self.primitiveTypes = ['boolean', 'int', 'byte', 'short', 'long', 'float', 'double', 'char']
        self.primitiveTypePattern = '|'.join(primitiveTypes)
        self.accessModMatcher = '(?P<access_modifier>public|private|protected)'
        self.objectType = '(?P<object_type>class|enum|interface)'
        self.fullyQualified = '(?P<full_name>[a-z](\.[a-z]*)+(?P<class_name>[A-Z][A-Za-z]+))'
        self.modifier = '(?P<modifier>abstract|static|final)'
        self.methodName = '(?P<method_name>[A-Za-z]+\()'
        self.fieldName = '(?P<field_name>[A-Za-z]+)'
        self.parameters = '(?P<parameters>(\,*' + self.fullyQualified + ')*)'
        self.exception = '(?P<exception>throws\s+(?P<exception_class>.*Exception))'
        self.compiledFrom = 'Compiled from (?P<source_name>[A-Z][A-Za-z]+\.java'
        self.signatureMatcher = self.accessModMatcher + '\s*' + self.objectType + '\s*' + self.fullyQualified + ' \{'
        self.methodMatcher = accessModMatcher + '\s*' + modifier + '\s*' \
            + '(?P<return_type>' + self.fullyQualified + ')' + '\s*' \
            + self.methodName + self.parameters + '\)\s*' + self.exception
        self.fieldMatcher = self.accessModMatcher + '\s*' + self.modifier + '\s*' \
            + '(?P<declared_type>' + self.fullyQualified + ')' + '\s*' \
            + self.methodName + self.parameters + '\)\s*' + self.exception
        self.staticUseless = 'static \{\}'
        self.end = '\}'


def get_fields_and_methods(className):
    with open('/Users/eric/.vim_indexes/javap_index.json', 'r') as javap_index:
        completionObj = json.load(javap_index)
        if className in completionObj.keys():
            return completionObj[className]
        return get_completions_for_class_name(className)


def get_class_file_path(className):
    with open('/Users/eric/.vim_indexes/java_class_index', 'r') as java_class_index:
        for path in java_class_index:
            file_name = path.split('/')[-1].split('.')[0]
            if className == file_name:
                path = path.replace('\n','')
                return path


def get_all_class_names(className):
    with open('/Users/eric/.vim_indexes/java_class_index', 'r') as java_class_index:
        file_names = []
        for path in java_class_index:
            file_name = path.split('/')[-1].split('.')[0]
            if file_name.beginswith(className):
                file_names.append(file_name)
        if len(file_names) > 0:
            return file_names
        return get_fuzzy_matches_for_class_name(className)


def get_fuzzy_matches_for_class_name(className):
    with open('/Users/eric/.vim_indexes/java_class_index', 'r') as java_class_index:
        fuzzy_matches = []
        for path in java_class_index:
            file_name = path.split('/')[-1].split('.')[0]
            ratio = SM(None, file_name, className)
            fuzzy_matches.append((ratio, file_name))
    return sorted(fuzzy_matches, key=lambda x: x[0])


def get_completions_for_class_name(className):
    filePath = get_class_file_path(className)
    completed = subprocess.run(['javap', filePath], capture_output=True, text=True)
    completion = parse_javap_output(completed, className)
    with open('/Users/eric/.vim_indexes/javap_index.json', 'r') as old_index:
        completionObj = json.load(old_index)
    completionObj[className] = completion
    with open('/Users/eric/.vim_indexes/javap_index.json', 'w') as old_index:
        json.dump(completionObj, old_index, indent=4)
    return completion


def parse_javap_output(completed: CompletedProcess, className: str):
    if completed.stderr:
        print('Error: ' + completed.stderr)
    lines = completed.stdout.split('\n')
    signature = lines[1]
    constructors = []
    methods = []
    fields = []
    mchs = JavapMatchers()
    for line in lines[2:-2]:
        methodMatch = re.compile(mchs.methodMatcher).fullmatch(line)
        fieldMatch = re.compile(mchs.fieldMatcher).fullmatch(line)
        useless = re.compile(mchs.end).fullmatch(line) \
            | re.compile(mchs.staticUseless).fullmatch(line) \
            | re.compile(mchs.compiledFrom).fullmatch(line)
        if methodMatch is not None:
            if className == methodMatch.groupdict()['method_name']:
                constructors.append(parse_constructor_line(methodMatch))
            else:
                methods.append(parse_method_line(fieldMatch))
        elif fieldMatch is not None:
            fields.append(parse_field_line(line))
        elif useless:
            pass
        else:
            raise Exception('Unhandled line type: {}'.format(line))
    completion = {}
    completion['constructors'] = constructors
    completion['methods'] = methods
    completion['fields'] = fields
    return completion


def parse_constructor_line(match: re.Match):
    d = match.groupdict()
    method['name'] = d['method_name']
    method['accessModifier'] = d['access_modifier']
    return method


def parse_method_line(methodMatch: re.Match):
    d = methodMatch.groupdict()
    parameters = d['parameters']
    methodName = d['method_name']
    methAndParams = methodName + '(' + ', '.join(parameters) + ')'
    method = {}
    method['name'] = methodName
    method['returnType'] = d['return_type']
    method['accessModifier'] = d['access_modifier']
    method['display'] = methAndParams
    method['displayMeta'] = returnType
    return method

def parse_field_line(fieldMatch: re.Match):
    d = fieldMatch.groupdict()
    field = {}
    field['name'] = d['field_name']
    field['type'] = d['declared_type']
    field['accessModifier'] = d['access_modifier']
    return field



