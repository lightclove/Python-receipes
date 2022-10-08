import re
import sys
# set up regular expressions
# use https://regexper.com to visualise these if required
parsed_dict = {

    'timestamp': re.compile(r'Grade = (?P<grade>\d+)\n'),

}

def printFile():
    with open(sys.argv[1]) as file:
        file_contents = file.read()
        print(file_contents)

def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def parse_file(filepath):
    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            key, match = _parse_line(line)
    return data

if __name__ == '__main__':
    print()
    try:
        #printFile()
        parse_file(sys.argv[1])
    except Exception as e:
        print('Something went wrong...')
        print('Exception caught: \n' + str(e).upper())
        print()
        print('Parser usage:')
        print('"python theParser.py [the File In The Current Dir]"')
        print('The option [the File In The Current Dir] is the second argument after python module name')


# from pyparsing import *
# module_name = Word(alphas + '_')
# full_module_name = module_name + ZeroOrMore('.' + module_name)
# import_as = Optional('as' + module_name)
# parse_module = 'import' + full_module_name + import_as
# s = 'import matplotlib.pyplot as plt'
# parse_module.parseString(s)
# print(parse_module.parseString(s).asList())
# full_module_name = module_name + ZeroOrMore(Suppress('.') + module_name)
# import_as = Optional(Suppress('as') + module_name)
# parse_module = Suppress('import') + full_module_name + import_as
# full_module_name = (module_name + ZeroOrMore(Suppress('.') + module_name))('modules')
# import_as = (Optional(Suppress('as') + module_name))('import_as')
# res = parse_module.parseString(s)
# print(res.modules.asList())
# print(res.import_as.asList())

# from pyparsing import Word, alphas, ZeroOrMore, Suppress, Optional
# module_name = Word(alphas + "_")
# full_module_name = (module_name + ZeroOrMore(Suppress('.') + module_name))('modules')
# import_as = (Optional(Suppress('as') + module_name))('import_as')
# parse_module = (Suppress('import') + full_module_name + import_as).setParseAction(lambda t: {'import': t.modules.asList(), 'as': t.import_as.asList()[0]})
# print(parse_module)
