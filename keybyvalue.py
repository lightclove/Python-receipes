# -*- coding: utf-8 -*-
#!/usr/bin/env python
def get_key_by_value(dict, value):
    for k, v in dict.items():
        if v == value:
            print "Found key: \"" + str(k) + "\" with type: " + str(type(k)) + " for the specified value: \"" + str(value)+"\"" + " in the dict: " + str(dict)
            return k
    else:
        print "Searched key for the value: \"" + str(value) + "\" not found in the dict: " + str(dict)

# Testing
dictionary = {1: '1', 2: '2', 3: '3'}
get_key_by_value(dictionary, '1')
#get_key_by_value(dictionary, '2')
#get_key_by_value(dictionary, '3')
#get_key_by_value(dictionary, 4)
#get_key_by_value(dictionary, '3')
#get_key_by_value(dictionary, '2')
#get_key_by_value(dictionary, '1')